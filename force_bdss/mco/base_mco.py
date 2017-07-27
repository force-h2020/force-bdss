import abc

from traits.api import ABCHasStrictTraits, Instance

from .i_mco_bundle import IMCOBundle


class BaseMCO(ABCHasStrictTraits):
    """Base class for the Multi Criteria Optimizer.

    Inherit this class for your MCO implementation
    """
    #: A reference to the bundle
    bundle = Instance(IMCOBundle)

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseMCO, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def run(self, model):
        """Reimplement this method to perform the MCO operations."""
        pass
