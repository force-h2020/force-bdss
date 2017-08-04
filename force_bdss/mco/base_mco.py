import abc

from traits.api import ABCHasStrictTraits, Instance

from .i_mco_factory import IMCOFactory


class BaseMCO(ABCHasStrictTraits):
    """Base class for the Multi Criteria Optimizer.

    Inherit this class for your MCO implementation
    """
    #: A reference to the bundle
    factory = Instance(IMCOFactory)

    def __init__(self, factory, *args, **kwargs):
        """Initializes the MCO.

        Parameters
        ----------
        factory: BaseMCOBundle
            The bundle this BaseMCO belongs to
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
