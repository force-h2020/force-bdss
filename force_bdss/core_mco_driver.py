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

    @on_trait_change("application:stopping")
    def application_stopping(self):
        for listener in self.listeners:
            try:
                listener.finalize(None)
            except Exception as e:
                logging.error(
                    "Failed to finalize "
                    "listener {}: {}".format(
                        listener.__class__.__name__, str(e)))

    def _mco_default(self):
        try:
            workflow = self.workflow
        except (InvalidVersionException, InvalidFileException) as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        mco_model = workflow.mco
        mco_factory = mco_model.factory
        return mco_factory.create_optimizer()

    @on_trait_change("mco:event")
    def _handle_mco_event(self, event):
        for listener in self.listeners:
            listener.deliver(None, event)

    def _listeners_default(self):
        listeners = []

        for factory in self.factory_registry.notification_listener_factories:
            try:
                listener = factory.create_listener()
                listener.initialize(None)
            except Exception as e:
                logging.error(
                    "Failed to create or initialize "
                    "listener with id {}: {}".format(
                        factory.id, str(e)))
            else:
                listeners.append(listener)

        return listeners
