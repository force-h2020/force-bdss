from traits.api import String
from force_bdss.api import bundle_id, BaseMultiCriteriaOptimizerBundle

from .dakota_communicator import DakotaCommunicator
from .dakota_model import DakotaModel
from .dakota_optimizer import DakotaOptimizer


class DakotaBundle(BaseMultiCriteriaOptimizerBundle):
    id = String(bundle_id("enthought", "dakota"))

    name = "Dakota"

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}
        return DakotaModel(self, **model_data)

    def create_optimizer(self, application, model):
        return DakotaOptimizer(self, application, model)

    def create_communicator(self, application, model):
        return DakotaCommunicator(self, application, model)
