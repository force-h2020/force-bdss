import abc

from traits.api import (
    ABCHasStrictTraits, Instance, Event, Dict, Unicode, Tuple)

from .i_mco_factory import IMCOFactory


class BaseMCO(ABCHasStrictTraits):
    """Base class for the Multi Criteria Optimizer.

    Inherit this class for your MCO implementation
    """
    #: A reference to the factory
    factory = Instance(IMCOFactory)

    #: Triggered when the evaluation started.
    started = Event()

    #: Triggered when the evaluation finished
    finished = Event()

    # Event triggered when the mco wants to send new data to listeners
    new_data = Event(Dict(Unicode(), Tuple()))

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
