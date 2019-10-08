import logging

from traits.api import (
    DelegatesTo, HasStrictTraits, Instance, List, on_trait_change, provides
)

from force_bdss.core.i_solver import ISolver
from force_bdss.core.workflow_solver import WorkflowSolver
from force_bdss.core_driver_events import MCOFinishEvent, MCOStartEvent
from force_bdss.mco.base_mco import BaseMCO
from force_bdss.notification_listeners.base_notification_listener import (
    BaseNotificationListener
)
from .i_operation import IOperation
from .workflow_file import WorkflowFile


log = logging.getLogger(__name__)


@provides(IOperation)
class OptimizeOperation(HasStrictTraits):
    """Performs a full MCO run on a system described by a `Workflow`
    object, based on the format given by a `BaseMCO` class. Contains
    optional `NotificationListener` classes in order to broadcast
    information during the MCO run."""

    #: The workflow file being operated on.
    workflow_file = Instance(WorkflowFile)

    #: The workflow instance.
    workflow = DelegatesTo('workflow_file')

    #: The mco instance.
    mco = Instance(BaseMCO)

    #: The notification listener instances.
    listeners = List(Instance(BaseNotificationListener))

    #: The Solver to use in the MCO run
    solver = Instance(ISolver)

    def _solver_default(self):
        return WorkflowSolver(
            workflow=self.workflow,
            workflow_filepath=self.workflow_file.path,
            executable_path='force_bdss',
            mode='Internal'
        )

    def run(self):
        """ Create and run the optimizer. """
        self.workflow_file.verify()
        if len(self.workflow_file.errors) != 0:
            log.error(
                "Unable to execute workflow due to verification errors:"
            )
            for error in self.workflow_file.errors:
                log.error(error.local_error)
            raise RuntimeError("Workflow file has errors.")

        mco_model = self.workflow.mco

        self.create_mco()

        self._deliver_start_event()

        try:
            self.mco.run(mco_model, self.solver)
        except Exception:
            log.exception((
                "Method run() of MCO with id '{}' from plugin '{}' "
                "raised exception. This might indicate a "
                "programming error in the plugin.").format(
                    self.mco.factory.id,
                    self.mco.factory.plugin_id
                )
            )
            raise
        finally:
            self._deliver_finish_event()
            self.destroy_mco()

    def create_mco(self):
        """ Create the MCO from the model's factory. """
        mco_factory = self.workflow.mco.factory
        try:
            self.mco = mco_factory.create_optimizer()
        except Exception:
            log.exception((
                "Unable to instantiate optimizer for mco '{}' in "
                "plugin '{}'. An exception was raised. "
                "This might indicate a programming error in the "
                "plugin.").format(
                    mco_factory.id,
                    mco_factory.plugin_id
                )
            )
            raise

        self._initialize_listeners()

    def destroy_mco(self):
        self._finalize_listeners()
        self.mco = None

    def _deliver_start_event(self):
        mco_model = self.workflow.mco
        self._deliver_event(MCOStartEvent(
            parameter_names=list(p.name for p in mco_model.parameters),
            kpi_names=list(kpi.name for kpi in mco_model.kpis)
        ))

    def _deliver_finish_event(self):
        self._deliver_event(MCOFinishEvent())

    @on_trait_change('mco:event')
    def _deliver_event(self, event):
        """ Delivers an event to the listeners """
        for listener in self.listeners[:]:
            try:
                listener.deliver(event)
            except Exception:
                log.exception((
                    "Exception while delivering to listener "
                    "'{}' in plugin '{}'. The listener will be dropped and "
                    "computation will continue.").format(
                        listener.factory.id,
                        listener.factory.plugin_id
                    )
                )
                self._finalize_listener(listener)
                self.listeners.remove(listener)

    def _finalize_listener(self, listener):
        """Helper method. Finalizes a listener and handles possible
        exceptions. it does _not_ remove the listener from the listener
        list.
        """
        try:
            listener.finalize()
        except Exception:
            log.exception((
                "Exception while finalizing listener '{}'"
                " in plugin '{}'.").format(
                    listener.factory.id,
                    listener.factory.plugin_id
                )
            )

    def _initialize_listeners(self):
        listeners = []

        for nl_model in self.workflow.notification_listeners:
            factory = nl_model.factory
            try:
                listener = factory.create_listener()
            except Exception:
                log.exception((
                    "Failed to create listener with id '{}' in plugin '{}'. "
                    "This may indicate a programming error in the "
                    "plugin.").format(
                        factory.id,
                        factory.plugin_id
                    )
                )
                raise

            try:
                listener.initialize(nl_model)
            except Exception:
                log.exception((
                    "Failed to initialize listener with id '{}' in "
                    "plugin '{}'. The listener will be dropped.").format(
                        factory.id,
                        factory.plugin_id
                    )
                )
                continue

            listeners.append(listener)

        self.listeners = listeners

    def _finalize_listeners(self):
        # finalize listeners
        for listener in self.listeners:
            self._finalize_listener(listener)
        self.listeners[:] = []
