from traits.api import Bool, Int, Function

from force_bdss.core.data_value import DataValue
from force_bdss.api import (
    BaseMCOModel, BaseMCO, BaseMCOFactory,
    BaseMCOParameter, BaseMCOParameterFactory,
    BaseMCOCommunicator
)


class ProbeMCOModel(BaseMCOModel):
    #: Counts how many times the edit_traits method has been called
    edit_traits_call_count = Int(0)

    def edit_traits(self, *args, **kwargs):
        self.edit_traits_call_count += 1


def run_func(*args, **kwargs):
    return []


class ProbeMCO(BaseMCO):
    run_function = Function(default_value=run_func)

    run_called = Bool(False)

    def run(self, model):
        self.run_called = True
        return self.run_function(model)


class ProbeParameter(BaseMCOParameter):
    pass


class ProbeParameterFactory(BaseMCOParameterFactory):
    def get_identifier(self):
        return "test"

    def get_model_class(self):
        return ProbeParameter


class ProbeMCOCommunicator(BaseMCOCommunicator):
    send_called = Bool(False)
    receive_called = Bool(False)

    nb_output_data_values = Int(0)

    def send_to_mco(self, model, kpi_results):
        self.send_called = True

    def receive_from_mco(self, model):
        self.receive_called = True
        return [
            DataValue() for _ in range(self.nb_output_data_values)
        ]


class ProbeMCOFactory(BaseMCOFactory):
    nb_output_data_values = Int(0)

    def get_identifier(self):
        return "test_mco"

    def get_model_class(self):
        return ProbeMCOModel

    def get_communicator_class(self):
        return ProbeMCOCommunicator

    def get_optimizer_class(self):
        return ProbeMCO

    def get_name(self):
        return "testmco"

    def create_communicator(self):
        return self.communicator_class(
            self,
            nb_output_data_values=self.nb_output_data_values)

    def parameter_factories(self):
        return [ProbeParameterFactory(mco_factory=self)]
