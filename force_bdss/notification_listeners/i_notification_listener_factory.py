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
        ".base_notification_listener.BaseNotificationListener"
    )

    model_class = Type(
        "force_bdss.notification_listeners"
        ".base_notification_listener_model.BaseNotificationListenerModel"
    )

    plugin = Instance(Plugin)

    def create_listener(self):
        """"""

    def create_model(self, model_data=None):
        """"""
