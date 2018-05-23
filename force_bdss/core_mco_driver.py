import sys
import logging

from traits.api import on_trait_change, Instance, List

from force_bdss.core.verifier import verify_workflow
from force_bdss.ids import InternalPluginID
from force_bdss.mco.base_mco import BaseMCO
from force_bdss.notification_listeners.base_notification_listener import \
    BaseNotificationListener
from .base_core_driver import BaseCoreDriver
from .core_driver_events import MCOStartEvent, MCOFinishEvent, MCOProgressEvent

log = logging.getLogger(__name__)


class CoreMCODriver(BaseCoreDriver):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """
    id = InternalPluginID.CORE_MCO_DRIVER_ID

    mco = Instance(BaseMCO, allow_none=True)

    listeners = List(Instance(BaseNotificationListener))

    @on_trait_change("application:started")
    def application_started(self):
        try:
            workflow = self.workflow
        except Exception:
            log.exception("Unable to open workflow file.")
            sys.exit(1)

        errors = verify_workflow(workflow)

        if len(errors) != 0:
            log.error("Unable to execute workflow due to verification "
                      "errors :")
            for err in errors:
                log.error(err.error)
            sys.exit(1)

        try:
            mco = self.mco
        except Exception:
            log.exception(
                "Unable to obtain MCO with id '{}' from plugin '{}'."
            )
            sys.exit(1)

        try:
            mco.run(self.workflow.mco)
        except Exception:
            log.exception(
                "Method run() of MCO with id '{}' from plugin '{}' "
                "raised exception. This might indicate a "
                "programming error in the plugin.".format(
                    mco.factory.id,
                    mco.factory.plugin.id))
            sys.exit(1)

    @on_trait_change("application:stopping")
    def application_stopping(self):
        for listener in self.listeners:
            self._finalize_listener(listener)
        self.listeners[:] = []

    def _mco_default(self):

        mco_model = self.workflow.mco
        if mco_model is None:
            log.info("No MCO defined. Nothing to do. Exiting.")
            sys.exit(0)

        mco_factory = mco_model.factory
        try:
            optimizer = mco_factory.create_optimizer()
        except Exception:
            log.exception("Unable to instantiate optimizer for mco '{}' in "
                          "plugin '{}'. An exception was raised. "
                          "This might indicate a programming error in the "
                          "plugin.".format(mco_factory.id,
                                           mco_factory.plugin.id))
            raise

        return optimizer

    @on_trait_change("mco:started")
    def _deliver_start_event(self):
        output_kpis = []
        for layer in self.workflow.execution_layers:
            for data_source in layer.data_sources:
                output_kpis.extend(
                    info for info in data_source.output_slot_info
                    if info.is_kpi
                )

        self._deliver_event(MCOStartEvent(
            input_names=tuple(p.name for p in self.workflow.mco.parameters),
            output_names=tuple([on.name for on in output_kpis])
        ))

    @on_trait_change("mco:finished")
    def _deliver_finished_event(self):
        self._deliver_event(MCOFinishEvent())

    @on_trait_change("mco:new_data")
    def _deliver_mco_progress_event(self, data):
        self._deliver_event(MCOProgressEvent(**data))

    def _deliver_event(self, event):
        """ Delivers an event to the listeners """
        for listener in self.listeners[:]:
            try:
                listener.deliver(event)
            except Exception:
                log.exception(
                    "Exception while delivering to listener "
                    "'{}' in plugin '{}'. The listener will be dropped and "
                    "computation will continue.".format(
                        listener.factory.id,
                        listener.factory.plugin.id
                    ))
                self._finalize_listener(listener)
                self.listeners.remove(listener)

    def _listeners_default(self):
        listeners = []

        for nl_model in self.workflow.notification_listeners:
            factory = nl_model.factory
            try:
                listener = factory.create_listener()
            except Exception:
                log.exception(
                    "Failed to create listener with id '{}' in plugin '{}'. "
                    "This may indicate a programming error in the "
                    "plugin.".format(
                        factory.id,
                        factory.plugin.id
                    )
                )
                raise

            try:
                listener.initialize(nl_model)
            except Exception:
                log.exception(
                    "Failed to initialize listener with id '{}' in "
                    "plugin '{}'. The listener will be dropped.".format(
                        factory.id,
                        factory.plugin.id
                    )
                )
                continue

            listeners.append(listener)

        return listeners

    def _finalize_listener(self, listener):
        """Helper method. Finalizes a listener and handles possible
        exceptions. it does _not_ remove the listener from the listener
        list.
        """
        try:
            listener.finalize()
        except Exception:
            log.exception(
                "Exception while finalizing listener '{}'"
                " in plugin '{}'.".format(
                    listener.factory.id,
                    listener.factory.plugin.id
                ))
