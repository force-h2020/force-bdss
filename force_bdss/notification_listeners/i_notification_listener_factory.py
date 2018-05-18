from traits.api import Interface, String, Instance, Type, Bool
from envisage.plugin import Plugin


class INotificationListenerFactory(Interface):
    """Envisage required interface for the BaseNotificationListenerFactory.
    You should not need to use this directly.

    Refer to the BaseNotificationListenerFactory for documentation.
    """
    id = String()

    name = String()

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

    plugin = Instance(Plugin, allow_none=False)

    def get_name(self):
        pass

    def get_identifier(self):
        pass

    def get_model_class(self):
        pass

    def get_listener_class(self):
        pass

    def create_listener(self):
        pass

    def create_model(self):
        pass
