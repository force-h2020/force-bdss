from traits.api import String
from force_bdss.api import factory_id, BaseMCOFactory
from force_bdss.core_plugins.dummy.dummy_dakota.parameters import \
    RangedMCOParameterFactory

from .dakota_communicator import DummyDakotaCommunicator
from .dakota_model import DummyDakotaModel
from .dakota_optimizer import DummyDakotaOptimizer


class DummyDakotaFactory(BaseMCOFactory):
    id = String(factory_id("enthought", "dummy_dakota"))

    name = "Dummy Dakota"

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}
        return DummyDakotaModel(self, **model_data)

    def create_optimizer(self):
        return DummyDakotaOptimizer(self)

    def create_communicator(self):
        return DummyDakotaCommunicator(self)

    def parameter_factories(self):
        return [
            RangedMCOParameterFactory(self)
        ]
