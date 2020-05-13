#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.core.data_value import DataValue
from force_bdss.events.base_driver_event import BaseDriverEvent
from force_bdss.notification_listeners.base_notification_listener import \
    BaseNotificationListener
from force_bdss.notification_listeners.base_notification_listener_factory \
    import \
    BaseNotificationListenerFactory
from force_bdss.notification_listeners.base_notification_listener_model \
    import \
    BaseNotificationListenerModel
from traits.trait_types import Int, Instance


class DummyNotificationListener(BaseNotificationListener):
    def deliver(self, event):
        pass


class DummyNotificationListenerModel(BaseNotificationListenerModel):
    pass


class DummyNotificationListenerFactory(BaseNotificationListenerFactory):
    def get_identifier(self):
        return "dummy_notification_listener"

    def get_name(self):
        return "Dummy notification listener"

    def get_listener_class(self):
        return DummyNotificationListener

    def get_model_class(self):
        return DummyNotificationListenerModel


class DummyEvent(BaseDriverEvent):
    stateless_data = Int(1)
    stateful_data = Instance(DataValue)
