from traits.api import String

from force_bdss.api import (
    factory_id,
    BaseNotificationListenerFactory)

from .dummy_notification_listener import DummyNotificationListener
from .dummy_notification_listener_model import DummyNotificationListenerModel


class DummyNotificationListenerFactory(BaseNotificationListenerFactory):
    id = String(factory_id("enthought", "dummy_notification_listener"))

    name = String("Dummy Notification Listener")

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}

        return DummyNotificationListenerModel(self, **model_data)

    def create_listener(self):
        return DummyNotificationListener(self)
