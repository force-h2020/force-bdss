import abc
import logging
import warnings

from traits.api import (
    ABCHasStrictTraits, Event, Instance
)

from force_bdss.core_driver_events import WeightedMCOProgressEvent

from .i_mco_factory import IMCOFactory


log = logging.getLogger(__name__)


class NotifyEventWarning:

    warning_message = (
        "Use of the BaseMCO.event attribute is now deprecated and will"
        " be removed in version 0.5.0. Please replace any uses of the "
        "BaseMCO.notify and BaseMCO.notify_new_point method with the "
        "equivalent BaseMCOModel.notify and "
        "BaseMCOModel.notify_new_point methods respectively"
    )

    @classmethod
    def warn(cls):
        log.warning(cls.warning_message)
        warnings.warn(cls.warning_message, DeprecationWarning)


class BaseMCO(ABCHasStrictTraits):
    """Base class for the Multi Criteria Optimizer.

    Inherit this class for your MCO implementation
    """
    #: A reference to the factory
    factory = Instance(IMCOFactory)

    event = Event()

    def __init__(self, factory, **traits):
        """Initializes the MCO.

        Parameters
        ----------
        factory: BaseMCOFactory
            The factory this BaseMCO belongs to
        """
        super(BaseMCO, self).__init__(factory=factory, **traits)

    @abc.abstractmethod
    def run(self, evaluator):
        """Performs the actual MCO operations.
        Re-implement this method to tailor to your MCO.

        Parameters
        ----------
        evaluator: IEvaluator
            An instance of a class providing an interface to IEvaluator,
            containing a BaseMCOModel instance as an attribute
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
        self.notify(
            WeightedMCOProgressEvent(
                optimal_point=optimal_point,
                optimal_kpis=optimal_kpis,
                weights=weights,
            )
        )

    def notify(self, event):
        """Notify the listeners with an event. The notification will be
        synchronous. All notification listeners will receive the event, one
        after another.

        Parameters
        ----------
        event: BaseMCOEvent
            The event to broadcast.
        """
        NotifyEventWarning.warn()
        self.event = event
