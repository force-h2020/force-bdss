import logging
from traits.api import (
    ABCHasStrictTraits, Instance, String, provides, Type, Bool
)
from envisage.plugin import Plugin

from force_bdss.notification_listeners.base_notification_listener import \
    BaseNotificationListener
from force_bdss.notification_listeners.base_notification_listener_model \
    import \
    BaseNotificationListenerModel
from .i_notification_listener_factory import INotificationListenerFactory

log = logging.getLogger(__name__)


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

    #: If the factor should be visible in the UI. Set to false to make it
    #: invisible. This is normally useful for notification systems that are
    #: not supposed to be configured by the user.
    ui_visible = Bool(True)

    #: The listener class that must be instantiated. Define this to your
    #: listener class.
    listener_class = Type(BaseNotificationListener)

    #: The associated model to the listener. Define this to your
    #: listener model class.
    model_class = Type(BaseNotificationListenerModel)

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

    def create_listener(self):
        """
        Creates an instance of the listener.
        """
        if self.listener_class is None:
            msg = ("listener_class cannot be None in {}. Either define "
                   "listener_class or reimplement create_listener on "
                   "your factory class.".format(self.__class__.__name__))
            log.error(msg)
            raise RuntimeError(msg)

        return self.listener_class(self)

    def create_model(self, model_data=None):
        """
        Creates an instance of the model.

        Parameters
        ----------
        model_data: dict
            Data to use to fill the model.
        """
        if model_data is None:
            model_data = {}

        if self.model_class is None:
            msg = ("model_class cannot be None in {}. Either define "
                   "model_class or reimplement create_model on your "
                   "factory class.".format(self.__class__.__name__))
            log.error(msg)
            raise RuntimeError(msg)

        return self.model_class(self, **model_data)
