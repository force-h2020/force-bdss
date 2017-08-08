from __future__ import print_function

import sys

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
        self.mco.run(self.workflow.mco)

    def _mco_default(self):
        try:
            workflow = self.workflow
        except (InvalidVersionException, InvalidFileException) as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        mco_model = workflow.mco
        mco_factory = mco_model.factory
        return mco_factory.create_optimizer()

    @on_trait_change("mco:started,mco:finished,mco:progress")
    def _handle_mco_event(self, object, name, old, new):
        if name == "started":
            self._deliver_to_listeners("MCO_STARTED")
        elif name == "finished":
            self._deliver_to_listeners("MCO_FINISHED")
        elif name == "progress":
            self._deliver_to_listeners("MCO_PROGRESS")

    def _deliver_to_listeners(self, message):
        for listener in self.listeners:
            listener.deliver(None, message)

    def _listeners_default(self):
        listeners = []

        print(self.factory_registry.notification_listener_factories)
        for factory in self.factory_registry.notification_listener_factories:
            listeners.append(factory.create_listener())

        return listeners
