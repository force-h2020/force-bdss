import sys
import logging

from traits.api import on_trait_change, Instance, List

from force_bdss.ids import InternalPluginID
from force_bdss.mco.base_mco import BaseMCO
from force_bdss.notification_listeners.base_notification_listener import \
    BaseNotificationListener
from .base_core_driver import BaseCoreDriver
from .io.workflow_reader import (
    InvalidVersionException,
    InvalidFileException
)
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
        self.mco.run(self.workflow.mco)

    @on_trait_change("application:stopping")
    def application_stopping(self):
        for listener in self.listeners:
            self._finalize_listener(listener)
        self.listeners[:] = []

    def _mco_default(self):
        try:
            workflow = self.workflow
        except (InvalidVersionException, InvalidFileException) as e:
            log.exception(e)
            sys.exit(1)

        mco_model = workflow.mco
        if mco_model is None:
            log.info("No MCO defined. Nothing to do. Exiting.")
            sys.exit(0)

        mco_factory = mco_model.factory
        return mco_factory.create_optimizer()

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
            except Exception as e:
                log.error(
                    "Exception while delivering to listener {}: {}".format(
                        listener.__class__.__name__,
                        str(e)
                    ))
                self._finalize_listener(listener)
                self.listeners.remove(listener)

    def _listeners_default(self):
        listeners = []

        for nl_model in self.workflow.notification_listeners:
            factory = nl_model.factory
            try:
                listener = factory.create_listener()
                listener.initialize(nl_model)
            except Exception as e:
                log.error(
                    "Failed to create or initialize "
                    "listener with id {}: {}".format(
                        factory.id, str(e)))
            else:
                listeners.append(listener)

        return listeners

    def _finalize_listener(self, listener):
        """Helper method. Finalizes a listener and handles possible
        exceptions. it does _not_ remove the listener from the listener
        list.
        """
        try:
            listener.finalize()
        except Exception as e:
            log.error(
                "Exception while finalizing listener {}: {}".format(
                    listener.__class__.__name__,
                    str(e)
                ))
