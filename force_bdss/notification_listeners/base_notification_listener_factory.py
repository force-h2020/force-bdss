import abc

from traits.api import ABCHasStrictTraits, Instance, String, provides
from envisage.plugin import Plugin

from .i_notification_listener_factory import INotificationListenerFactory


@provides(INotificationListenerFactory)
class BaseNotificationListenerFactory(ABCHasStrictTraits):
    """Base class for notification listeners.
    Notification listeners are extensions that receive event notifications
    from the MCO and perform an associated action.
    """
    #: identifier of the factory
    id = String()

    #: Name of the factory. User friendly for UI
    name = String()

    #: A reference to the containing plugin
    plugin = Instance(Plugin)

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
        """
        Creates an instance of the listener.
        """

    @abc.abstractmethod
    def create_model(self, model_data=None):
        """
        Creates an instance of the model.

        Parameters
        ----------
        model_data: dict
            Data to use to fill the model.
        """
