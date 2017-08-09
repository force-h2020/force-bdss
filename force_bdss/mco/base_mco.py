import abc

from traits.api import ABCHasStrictTraits, Instance, Event

from force_bdss.mco.events import BaseMCOEvent
from .i_mco_factory import IMCOFactory


class BaseMCO(ABCHasStrictTraits):
    """Base class for the Multi Criteria Optimizer.

    Inherit this class for your MCO implementation
    """
    #: A reference to the factory
    factory = Instance(IMCOFactory)

    #: Triggered when an event occurs.
    event = Event(BaseMCOEvent)

    def __init__(self, factory, *args, **kwargs):
        """Initializes the MCO.

        Parameters
        ----------
        factory: BaseMCOFactory
            The factory this BaseMCO belongs to
        """
        self.factory = factory
        super(BaseMCO, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def run(self, model):
        """Performs the actual MCO operations.
        Reimplement this method to tailor to your MCO.

        Parameters
        ----------
        model: BaseMCOModel
            An instance of the model information, as created from
            create_model()
        """

    def notify_event(self, event):
        """Method based interface to deliver an event, instead of
        assignment to traits.

        Sends the event, synchronously. When the routine returns,
        listeners have been fully informed (they might, however, handle
        the event asynchronously at their convenience)

        Parameters
        ----------
        event: BaseMCOEvent
            The event to deliver.
        """
        self.event = event
