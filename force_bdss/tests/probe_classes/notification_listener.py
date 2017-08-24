from traits.api import Bool, Str, Type

from force_bdss.ids import factory_id
from force_bdss.api import (
    BaseNotificationListener, BaseNotificationListenerModel,
    BaseNotificationListenerFactory)


class ProbeNotificationListener(BaseNotificationListener):
    initialize_called = Bool(False)
    deliver_called = Bool(False)
    finalize_called = Bool(False)

    def initialize(self, model):
        self.initialize_called = True

    def deliver(self, event):
        self.deliver_called = True

    def finalize(self):
        self.finalize_called = True


class ProbeNotificationListenerModel(BaseNotificationListenerModel):
    pass


class ProbeNotificationListenerFactory(BaseNotificationListenerFactory):
    id = Str(factory_id("enthought", "test_nl"))
    name = "test_notification_listener"

    model_class = Type(ProbeNotificationListenerModel)

    listener_class = Type(ProbeNotificationListener)

    def create_listener(self):
        return self.listener_class(self)

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}
        return self.model_class(self, **model_data)
