from traits.api import Interface, String, Instance, Any
from envisage.plugin import Plugin


class INotificationListenerFactory(Interface):
    """Envisage required interface for the BaseNotificationListenerFactory.
    You should not need to use this directly.

    Refer to the BaseNotifier for documentation.
    """
    id = String()

    name = String()

    plugin = Instance(Plugin)

    persistent_state = Any

    def create_listener(self):
        """"""

    def create_model(self, model_data=None):
        """"""

    def init_persistent_state(self):
        pass
