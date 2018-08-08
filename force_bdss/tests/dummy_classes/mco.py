from traits.api import Int
from force_bdss.mco.base_mco import BaseMCO
from force_bdss.mco.base_mco_communicator import BaseMCOCommunicator
from force_bdss.mco.base_mco_factory import BaseMCOFactory
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory


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


class DummyMCOParameter(BaseMCOParameter):
    x = Int()


class DummyMCOParameterFactory(BaseMCOParameterFactory):
    def get_identifier(self):
        return "dummy_mco_parameter"

    def get_name(self):
        return "Dummy MCO parameter"

    def get_description(self):
        return "description"

    def get_model_class(self):
        return DummyMCOParameter


class DummyMCOFactory(BaseMCOFactory):
    def get_identifier(self):
        return "dummy_mco"

    def get_name(self):
        return "Dummy MCO"

    def get_model_class(self):
        return DummyMCOModel

    def get_communicator_class(self):
        return DummyMCOCommunicator

    def get_optimizer_class(self):
        return DummyMCO

    def get_parameter_factory_classes(self):
        return [DummyMCOParameterFactory]
