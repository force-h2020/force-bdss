from traits.api import Bool, Str, Type

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
    id = Str("enthought.test.notification_listener")
    name = "test_notification_listener"

    model_class = Type(ProbeNotificationListenerModel)

    listener_class = Type(ProbeNotificationListener)

    def create_listener(self):
        return self.listener_class(self)

    def create_model(self, model_data=None):
        return self.model_class(self, model_data=model_data)
