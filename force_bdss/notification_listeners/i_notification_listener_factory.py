from traits.api import Type, Bool

from force_bdss.core.i_factory import IFactory


class INotificationListenerFactory(IFactory):
    """Envisage required interface for the BaseNotificationListenerFactory.
    You should not need to use this directly.

    Refer to the BaseNotificationListenerFactory for documentation.
    """
    ui_visible = Bool()

    listener_class = Type(
        "force_bdss.notification_listeners"
        ".base_notification_listener.BaseNotificationListener",
        allow_none=False,
    )

    model_class = Type(
        "force_bdss.notification_listeners"
        ".base_notification_listener_model.BaseNotificationListenerModel",
        allow_none=False
    )

    def get_model_class(self):
        pass

    def get_listener_class(self):
        pass

    def create_listener(self):
        pass

    def create_model(self):
        pass
