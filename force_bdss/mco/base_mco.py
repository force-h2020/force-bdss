import abc

from traits.api import ABCHasStrictTraits, Instance, Event

from force_bdss.core_driver_events import MCOProgressEvent
from .i_mco_factory import IMCOFactory


class BaseMCO(ABCHasStrictTraits):
    """Base class for the Multi Criteria Optimizer.

    Inherit this class for your MCO implementation
    """
    #: A reference to the factory
    factory = Instance(IMCOFactory)

    #: Propagation channel for events from the MCO
    event = Event()

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

    def notify_new_point(self, optimal_point, optimal_kpis, weights):
        """Notify the discovery of a new optimal point.

        Parameters
        ----------
        optimal_point: List(Instance(DataValue))
            A list of DataValue objects describing the point in parameter
            space that produces an optimised result.

        optimal_kpis: List(Instance(DataValue))
            A list of DataValue objects describing the KPI values resulting
            from the optimal_point values above.

        weights: List(Float())
            A list of weight values from 0.0 to 1.0 that have been assigned
            for this point to each KPI.
        """
        self.notify(MCOProgressEvent(
            optimal_point=optimal_point,
            optimal_kpis=optimal_kpis,
            weights=weights,
        ))

    def notify(self, event):
        """Notify the listeners with an event. The notification will be
        synchronous. All notification listeners will receive the event, one
        after another.

        Parameters
        ----------
        event: BaseMCOEvent
            The event to broadcast.
        """
        self.event = event
