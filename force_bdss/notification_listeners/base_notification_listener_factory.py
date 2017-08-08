import abc

from traits.api import ABCHasStrictTraits, Instance, String, provides, Any
from envisage.plugin import Plugin

from .i_notification_listener_factory import INotificationListenerFactory


@provides(INotificationListenerFactory)
class BaseNotificationListenerFactory(ABCHasStrictTraits):
    id = String()

    name = String()

    plugin = Instance(Plugin)

    persistent_state = Any()

    def __init__(self, plugin, *args, **kwargs):
        """Initializes the instance.

        Parameters
        ----------
        plugin: Plugin
            The plugin that holds this factory.
        """
        self.plugin = plugin
        super(BaseNotificationListenerFactory, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def create_listener(self):
        """"""

    @abc.abstractmethod
    def create_model(self, model_data=None):
        """"""

    def init_persistent_state(self):
        pass
