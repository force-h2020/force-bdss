from traits.api import Bool, Str, Type, Function, Any

from force_bdss.ids import factory_id
from force_bdss.api import (
    BaseNotificationListener, BaseNotificationListenerModel,
    BaseNotificationListenerFactory)


def pass_function(*args, **kwargs):
    pass


class ProbeNotificationListener(BaseNotificationListener):
    initialize_called = Bool(False)
    deliver_called = Bool(False)
    finalize_called = Bool(False)

    initialize_function = Function(default_value=pass_function)
    deliver_function = Function(default_value=pass_function)
    finalize_function = Function(default_value=pass_function)

    initialize_call_args = Any()
    deliver_call_args = Any()
    finalize_call_args = Any(([], {}))

    def initialize(self, model):
        self.initialize_called = True
        self.initialize_call_args = ([model], {})
        self.initialize_function(model)

    def deliver(self, event):
        self.deliver_called = True
        self.deliver_call_args = ([event], {})
        self.deliver_function(event)

    def finalize(self):
        self.finalize_called = True
        self.finalize_function()


class ProbeNotificationListenerModel(BaseNotificationListenerModel):
    pass


class ProbeNotificationListenerFactory(BaseNotificationListenerFactory):
    id = Str(factory_id("enthought", "test_nl"))
    name = "test_notification_listener"

    model_class = Type(ProbeNotificationListenerModel)

    listener_class = Type(ProbeNotificationListener)

    initialize_function = Function(default_value=pass_function)
    deliver_function = Function(default_value=pass_function)
    finalize_function = Function(default_value=pass_function)

    def create_listener(self):
        return self.listener_class(
            self,
            initialize_function=self.initialize_function,
            deliver_function=self.deliver_function,
            finalize_function=self.finalize_function)

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}
        return self.model_class(self, **model_data)
