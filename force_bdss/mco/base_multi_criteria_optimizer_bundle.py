import abc

from traits.api import ABCHasStrictTraits, String
from traits.has_traits import provides

from force_bdss.mco.i_multi_criteria_optimizer_bundle import (
    IMultiCriteriaOptimizerBundle
)


@provides(IMultiCriteriaOptimizerBundle)
class BaseMultiCriteriaOptimizerBundle(ABCHasStrictTraits):
    id = String()

    name = String()

    @abc.abstractmethod
    def create_optimizer(self, application, model):
        pass

    @abc.abstractmethod
    def create_model(self, model_data=None):
        pass

    @abc.abstractmethod
    def create_communicator(self, model_data):
        pass
