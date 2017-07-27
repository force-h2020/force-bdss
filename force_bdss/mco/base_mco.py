import abc

from traits.api import ABCHasStrictTraits, Instance

from ..bdss_application import BDSSApplication
from .base_mco_model import BaseMCOModel
from .i_mco_bundle import IMCOBundle


class BaseMCO(ABCHasStrictTraits):
    """Base class for the Multi Criteria Optimizer.

    Inherit this class for your MCO implementation
    """
    #: A reference to the bundle
    bundle = Instance(IMCOBundle)
    #: A reference to the application
    application = Instance(BDSSApplication)
    #: A reference to the model class
    model = Instance(BaseMCOModel)

    def __init__(self, bundle, application, model, *args, **kwargs):
        self.bundle = bundle
        self.application = application
        self.model = model
        super(BaseMCO, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def run(self):
        """Reimplement this method to perform the MCO operations."""
        pass
