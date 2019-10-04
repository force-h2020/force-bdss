from traits.api import Bool, Function, Any

from force_bdss.api import (
    BaseNotificationListener, BaseNotificationListenerModel,
    BaseNotificationListenerFactory)


def pass_function(*args, **kwargs):
    pass


def raise_exception(*args, **kwargs):
    raise Exception()


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
    initialize_function = Function(default_value=pass_function)
    deliver_function = Function(default_value=pass_function)
    finalize_function = Function(default_value=pass_function)

    raises_on_create_model = Bool(False)
    raises_on_create_listener = Bool(False)

    raises_on_initialize_listener = Bool(False)
    raises_on_finalize_listener = Bool(False)
    raises_on_deliver_listener = Bool(False)

    def get_name(self):
        return "test_notification_listener"

    def get_identifier(self):
        return "probe_notification_listener"

    def get_listener_class(self):
        return ProbeNotificationListener

    def get_model_class(self):
        return ProbeNotificationListenerModel

    def create_model(self, model_data=None):
        if self.raises_on_create_model:
            raise Exception("ProbeNotificationListenerFactory.create_model")

        if model_data is None:
            model_data = {}

        return self.model_class(self, **model_data)

    def create_listener(self):
        if self.raises_on_create_listener:
            raise Exception("ProbeNotificationListenerFactory.create_listener")

        if self.raises_on_initialize_listener:
            initialize_function = raise_exception
        else:
            initialize_function = self.initialize_function

        if self.raises_on_finalize_listener:
            finalize_function = raise_exception
        else:
            finalize_function = self.finalize_function

        if self.raises_on_deliver_listener:
            deliver_function = raise_exception
        else:
            deliver_function = self.deliver_function

        return self.listener_class(
            self,
            initialize_function=initialize_function,
            deliver_function=deliver_function,
            finalize_function=finalize_function)
