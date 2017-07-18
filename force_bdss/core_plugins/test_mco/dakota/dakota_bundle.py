from traits.has_traits import HasStrictTraits, provides
from traits.trait_types import String

from force_bdss.core_plugins.test_mco.dakota.dakota_communicator import \
    DakotaCommunicator
from force_bdss.mco.i_multi_criteria_optimizer_bundle import (
    IMultiCriteriaOptimizerBundle)

from .dakota_model import DakotaModel
from .dakota_optimizer import DakotaOptimizer


@provides(IMultiCriteriaOptimizerBundle)
class DakotaBundle(HasStrictTraits):
    name = String("dakota")

    def create_model(self, model_data=None):
        if model_data is None:
            return DakotaModel()
        else:
            return DakotaModel.from_json(model_data)

    def create_optimizer(self, application, model):
        return DakotaOptimizer(self, application, model)

    def create_communicator(self, application, model):
        return DakotaCommunicator(self, application, model)
