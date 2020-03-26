import logging
import sys
from threading import Event as ThreadingEvent

from traits.api import (
    DelegatesTo,
    HasStrictTraits,
    Instance,
    List,
    on_trait_change,
    provides,
)

from force_bdss.notification_listeners.base_notification_listener import (
    BaseNotificationListener,
)
from force_bdss.ui_hooks.ui_notification_mixins import (
    UIEventNotificationMixin
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
    workflow = DelegatesTo("workflow_file")

    #: The notification listener instances.
    listeners = List(Instance(BaseNotificationListener))

    #: Threading Event instance that indicates if the optimization operation
    #: should be stopped.
    _stop_event = Instance(ThreadingEvent, visible=False, transient=True)

    #: Threading Event instance that indicates if the optimization operation
    #: should be paused and then resumed.
    _pause_event = Instance(ThreadingEvent, visible=False, transient=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = ThreadingEvent()
        self._pause_event = ThreadingEvent()
        self._pause_event.set()

    def run(self):
        """ Create and run the optimizer. """
        self.workflow_file.verify()
        if len(self.workflow_file.errors) != 0:
            log.error("Unable to execute workflow due to verification errors:")
            for error in self.workflow_file.errors:
                log.error(error.local_error)
            raise RuntimeError("Workflow file has errors.")

        mco = self.create_mco()
        self._deliver_start_event()

        try:
            mco.run(self.workflow)
        except Exception:
            log.exception(
                (
                    "Method run() of MCO with id '{}' from plugin '{}' "
                    "raised exception. This might indicate a "
                    "programming error in the plugin."
                ).format(mco.factory.id, mco.factory.plugin_id)
            )
            raise
        finally:
            self._deliver_finish_event()
            self._finalize_listeners()

    def create_mco(self):
        """ Create the MCO from the model's factory. """
        mco_factory = self.workflow.mco_model.factory
        try:
            mco = mco_factory.create_optimizer()
        except Exception:
            log.exception(
                (
                    "Unable to instantiate optimizer for mco '{}' in "
                    "plugin '{}'. An exception was raised. "
                    "This might indicate a programming error in the "
                    "plugin."
                ).format(mco_factory.id, mco_factory.plugin_id)
            )
            raise

        self._initialize_listeners()

        return mco

    def _deliver_start_event(self):
        self.workflow.mco_model.notify_start_event()

    def _deliver_finish_event(self):
        self.workflow.mco_model.notify_finish_event()

    @on_trait_change("workflow_file:workflow:event")
    def _deliver_event(self, event):
        """ Events fired by the workflow_file.workflow are the communication
        entry points with the BDSS execution process.
        Delivers an event to the listeners, and performs the
        control events check after the `event` is delivered.
        """
        for listener in self.listeners[:]:
            try:
                listener.deliver(event)
            except Exception:
                log.exception(
                    (
                        f"Exception while delivering to listener "
                        f"'{listener.factory.id}' in plugin "
                        f"'{listener.factory.plugin_id}'. The listener will "
                        f"be dropped and computation will continue."
                    )
                )
                self._finalize_listener(listener)
                self.listeners.remove(listener)

        self.ui_event_response()

    def ui_event_response(self):
        """ Checks the status of the _pause_event and _stop_event
        attributes. Pauses the BDSS execution until the _pause_event is set.
        Terminates the OptimizeOperation if the _stop_event is set.
        """
        self._pause_event.wait()

        if self._stop_event.is_set():
            self._finalize_listeners()
            sys.exit("BDSS stopped")

    def _finalize_listener(self, listener):
        """Helper method. Finalizes a listener and handles possible
        exceptions. it does _not_ remove the listener from the listener
        list.
        """
        try:
            listener.finalize()
        except Exception:
            log.exception(
                (
                    "Exception while finalizing listener '{}'"
                    " in plugin '{}'."
                ).format(listener.factory.id, listener.factory.plugin_id)
            )

    def _set_threading_events(self, listener):
        """Assign stop and pause threading events to
        a UIEventNotificationMixin listener"""
        listener.set_stop_event(self._stop_event)
        listener.set_pause_event(self._pause_event)

    def _initialize_listeners(self):
        listeners = []

        for nl_model in self.workflow.notification_listeners:
            factory = nl_model.factory
            try:
                listener = factory.create_listener()
            except Exception:
                log.exception(
                    (
                        f"Failed to create listener with id '{factory.id}' "
                        f"in plugin '{factory.plugin_id}'. "
                        "This may indicate a programming error in the "
                        "plugin."
                    )
                )
                raise

            if isinstance(listener, UIEventNotificationMixin):
                self._set_threading_events(listener)

            try:
                listener.initialize(nl_model)
            except Exception:
                log.exception(
                    (
                        "Failed to initialize listener with id '{}' in "
                        "plugin '{}'. The listener will be dropped."
                    ).format(factory.id, factory.plugin_id)
                )
                continue

            listeners.append(listener)

        self.listeners = listeners

    def _finalize_listeners(self):
        # finalize listeners
        for listener in self.listeners:
            self._finalize_listener(listener)
        self.listeners[:] = []
