import abc

from traits.api import ABCHasStrictTraits, Instance

from ..bdss_application import BDSSApplication
from .base_mco_model import BaseMCOModel
from .i_multi_criteria_optimizer_bundle import IMultiCriteriaOptimizerBundle


class BaseMultiCriteriaOptimizer(ABCHasStrictTraits):
    """Base class for the Multi Criteria Optimizer.

    Inherit this class for your MCO implementation
    """
    #: A reference to the bundle
    bundle = Instance(IMultiCriteriaOptimizerBundle)
    #: A reference to the application
    application = Instance(BDSSApplication)
    #: A reference to the model class
    model = Instance(BaseMCOModel)

    def __init__(self, bundle, application, model, *args, **kwargs):
        self.bundle = bundle
        self.application = application
        self.model = model
        super(BaseMultiCriteriaOptimizer, self).__init__(*args, **kwargs)

    @property
    def name(self):
        """Convenience property to return the name of the bundle from the
        MCO itself"""
        return self.bundle.name

    @abc.abstractmethod
    def run(self):
        """Reimplement this method to perform the MCO operations."""
        pass
