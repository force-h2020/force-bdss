from traits.api import String
from force_bdss.api import bundle_id, BaseMCOBundle

from .dakota_communicator import DummyDakotaCommunicator
from .dakota_model import DummyDakotaModel
from .dakota_optimizer import DummyDakotaOptimizer


class DummyDakotaBundle(BaseMCOBundle):
    id = String(bundle_id("enthought", "dummy_dakota"))

    name = "Dummy Dakota"

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}
        return DummyDakotaModel(self, **model_data)

    def create_optimizer(self, application, model):
        return DummyDakotaOptimizer(self, application, model)

    def create_communicator(self, application, model):
        return DummyDakotaCommunicator(self, application, model)
