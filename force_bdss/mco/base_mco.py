import abc
import logging

from traits.api import (
    ABCHasStrictTraits, Instance
)

from .i_mco_factory import IMCOFactory


log = logging.getLogger(__name__)


class BaseMCO(ABCHasStrictTraits):
    """Base class for the Multi Criteria Optimizer.

    Inherit this class for your MCO implementation
    """
    #: A reference to the factory
    factory = Instance(IMCOFactory)

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
        Re-implement this method to tailor to your MCO. Use the
        evaluator.mco_model API to notify the BDSS of any MCO related
        BaseDriverEvents.

        Parameters
        ----------
        evaluator: IEvaluator
            An instance of a class providing an interface to IEvaluator,
            containing a BaseMCOModel instance as an attribute
        """
