from traits.has_traits import HasStrictTraits, provides

from force_bdss.mco.dakota_optimizer import DakotaOptimizer
from force_bdss.mco.dakota_model import DakotaModel
from .i_multi_criteria_optimizer_bundle import IMultiCriteriaOptimizerBundle


@provides(IMultiCriteriaOptimizerBundle)
class DakotaBundle(HasStrictTraits):
    def create_model(self, model_data):
        return DakotaModel.from_json(model_data)

    def create_ui(self):
        pass

    def create_optimizer(self, application, model):
        return DakotaOptimizer(self, application, model)
