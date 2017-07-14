from traits.has_traits import HasStrictTraits, provides

from .i_multi_criteria_optimizer_bundle import IMultiCriteriaOptimizerBundle
from .basic_model import BasicModel
from .basic_optimizer import BasicOptimizer


@provides(IMultiCriteriaOptimizerBundle)
class BasicBundle(HasStrictTraits):
    def create_model(self, model_data):
        return BasicModel.from_json(model_data)

    def create_ui(self):
        pass

    def create_optimizer(self, application, model):
        return BasicOptimizer(self, application, model)
