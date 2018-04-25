from traits.api import Interface, String, Instance
from envisage.plugin import Plugin

from force_bdss.notification_listeners.base_notification_listener import \
    BaseNotificationListener
from force_bdss.notification_listeners.base_notification_listener_model \
    import \
    BaseNotificationListenerModel


class INotificationListenerFactory(Interface):
    """Envisage required interface for the BaseNotificationListenerFactory.
    You should not need to use this directly.

    Refer to the BaseNotificationListenerFactory for documentation.
    """
    id = String()

    name = String()

    listener_class = Instance(BaseNotificationListener)

    model_class = Instance(BaseNotificationListenerModel)

    plugin = Instance(Plugin)

    def create_listener(self):
        """"""

    def create_model(self, model_data=None):
        """"""
