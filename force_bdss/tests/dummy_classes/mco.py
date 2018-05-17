from force_bdss.mco.base_mco import BaseMCO
from force_bdss.mco.base_mco_communicator import BaseMCOCommunicator
from force_bdss.mco.base_mco_factory import BaseMCOFactory
from force_bdss.mco.base_mco_model import BaseMCOModel


class DummyMCO(BaseMCO):
    def run(self, model, *args, **kwargs):
        pass


class DummyMCOCommunicator(BaseMCOCommunicator):
    def receive_from_mco(self, model):
        pass

    def send_to_mco(self, model, kpi_results):
        pass


class DummyMCOModel(BaseMCOModel):
    pass


class DummyMCOFactory(BaseMCOFactory):
    def get_identifier(self):
        return "foo"

    def get_name(self):
        return "bar"

    def get_model_class(self):
        return DummyMCOModel

    def get_communicator_class(self):
        return DummyMCOCommunicator

    def get_optimizer_class(self):
        return DummyMCO

    def parameter_factories(self):
        return []
