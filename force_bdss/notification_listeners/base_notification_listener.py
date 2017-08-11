import abc

from traits.api import ABCHasStrictTraits, Instance

from .i_notification_listener_factory import INotificationListenerFactory


class BaseNotificationListener(ABCHasStrictTraits):
    """Base class for the Notification Listener.

    Inherit this class for your MCO implementation
    """
    #: A reference to the factory
    factory = Instance(INotificationListenerFactory)

    def __init__(self, factory, *args, **kwargs):
        """Initializes the MCO.

        Parameters
        ----------
        factory: BaseMCOFactory
            The factory this BaseMCO belongs to
        """
        self.factory = factory
        super(BaseNotificationListener, self).__init__(*args, **kwargs)

    def initialize(self, model):
        """
        Method used to initialize persistent state of the listener using
        information from the model.

        Reimplement it in your Notification Listener to perform special
        initialization of state that survives across deliver() invocations,
        such as setting up a connection, or opening a file.
        """

    def finalize(self):
        """
        Method used to finalize state of the listener.

        Reimplement it in your Notification Listener to perform special
        finalization of state that survives across deliver() invocations,
        such as closing a connection, or closing a file.
        """

    @abc.abstractmethod
    def deliver(self, event):
        """Delivers the event to the recipient

        Parameters
        ----------
        event: MCOEvent
            The event to notify.
        """
