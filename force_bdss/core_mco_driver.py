from __future__ import print_function

import sys
import logging

from traits.api import on_trait_change, Instance, List

from force_bdss.mco.base_mco import BaseMCO
from force_bdss.notification_listeners.base_notification_listener import \
    BaseNotificationListener
from .ids import plugin_id
from .base_core_driver import BaseCoreDriver
from .io.workflow_reader import (
    InvalidVersionException,
    InvalidFileException
)
from .core_driver_events import MCOStartEvent, MCOFinishEvent, MCOProgressEvent

log = logging.getLogger(__name__)
CORE_MCO_DRIVER_ID = plugin_id("core", "CoreMCODriver")


class CoreMCODriver(BaseCoreDriver):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """
    id = CORE_MCO_DRIVER_ID

    mco = Instance(BaseMCO, allow_none=True)

    listeners = List(Instance(BaseNotificationListener))

    @on_trait_change("application:started")
    def application_started(self):
        self._deliver_start_event()
        self.mco.run(self.workflow.mco)
        self._deliver_event(MCOFinishEvent())

    @on_trait_change("application:stopping")
    def application_stopping(self):
        for listener in self.listeners:
            self._finalize_listener(listener)
        self.listeners[:] = []

    def _mco_default(self):
        try:
            workflow = self.workflow
        except (InvalidVersionException, InvalidFileException) as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        mco_model = workflow.mco
        mco_factory = mco_model.factory
        return mco_factory.create_optimizer()

    def _deliver_start_event(self):
        output_names = []
        for kpi in self.workflow.kpi_calculators:
            output_names.extend(kpi.output_slot_names)

        self._deliver_event(MCOStartEvent(
            input_names=[p.name for p in self.workflow.mco.parameters],
            output_names=output_names
        ))

    @on_trait_change("mco:new_data")
    def _deliver_progress_event(self, event):
        self._deliver_event(MCOProgressEvent(
            input=event['input'],
            output=event['output']
        ))

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
