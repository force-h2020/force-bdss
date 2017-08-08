import abc

from traits.api import ABCHasStrictTraits, Instance

from .i_notification_listener_factory import INotificationListenerFactory


class BaseNotificationListener(ABCHasStrictTraits):
    """Base class for the Multi Criteria Optimizer.

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

    @abc.abstractmethod
    def deliver(self, model, message):
        pass
