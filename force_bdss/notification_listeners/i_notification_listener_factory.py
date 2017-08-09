from traits.api import Interface, String, Instance
from envisage.plugin import Plugin


class INotificationListenerFactory(Interface):
    """Envisage required interface for the BaseNotificationListenerFactory.
    You should not need to use this directly.

    Refer to the BaseNotificationListenerFactory for documentation.
    """
    id = String()

    name = String()

    plugin = Instance(Plugin)

    def create_listener(self):
        """"""

    def create_model(self, model_data=None):
        """"""
