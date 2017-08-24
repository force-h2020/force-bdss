from traits.api import Str, Type, Bool, Int, Function

from force_bdss.ids import mco_parameter_id, factory_id
from force_bdss.core.data_value import DataValue
from force_bdss.api import (
    BaseMCOModel, BaseMCO, BaseMCOFactory,
    BaseMCOParameter, BaseMCOParameterFactory,
    BaseMCOCommunicator
)


class ProbeMCOModel(BaseMCOModel):
    pass


def run_func(*args, **kwargs):
    return []


class ProbeMCO(BaseMCO):
    run_function = Function()

    run_called = Bool(False)

    def __init__(self, factory, run_function=None, *args, **kwargs):
        if run_function is None:
            self.run_function = run_func
        super(ProbeMCO, self).__init__(self, factory, *args, **kwargs)

    def run(self, model):
        self.run_called = True

    def _run_function_default(self):
        def run_func(*args, **kwargs):
            pass
        return run_func


class ProbeParameter(BaseMCOParameter):
    pass


class RangedParameterFactory(BaseMCOParameterFactory):
    id = Str(mco_parameter_id("enthought", "test_mco", "test"))

    model_class = Type(ProbeParameter)


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
    id = Str(factory_id("enthought", "test_mco"))

    model_class = Type(ProbeMCOModel)

    communicator_class = Type(ProbeMCOCommunicator)

    mco_class = Type(ProbeMCO)

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}
        return self.model_class(
            self,
            **model_data
        )

    def create_communicator(self):
        return self.communicator_class(self)

    def create_optimizer(self):
        return self.mco_class(self)

    def parameter_factories(self):
        return []
