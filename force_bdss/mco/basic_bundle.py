from traits.has_traits import HasStrictTraits, provides
from traits.trait_types import String

from .i_multi_criteria_optimizer_bundle import IMultiCriteriaOptimizerBundle
from .basic_model import BasicModel
from .basic_optimizer import BasicOptimizer


@provides(IMultiCriteriaOptimizerBundle)
class BasicBundle(HasStrictTraits):
    name = String("basic")

    def create_model(self, model_data):
        return BasicModel.from_json(model_data)

    def create_ui(self):
        pass

    def create_optimizer(self, application, model):
        return BasicOptimizer(self, application, model)
