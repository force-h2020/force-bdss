from traits.api import Interface, String, Instance
from envisage.plugin import Plugin


class INotificationListenerFactory(Interface):
    """Envisage required interface for the BaseNotificationListenerFactory.
    You should not need to use this directly.

    Refer to the BaseNotifier for documentation.
    """
    id = String()

    name = String()

    plugin = Instance(Plugin)

    def create_object(self):
        """"""

    def create_model(self, model_data=None):
        """"""
