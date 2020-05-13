#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Bool, Int, Function, Any

from force_bdss.core.data_value import DataValue
from force_bdss.api import (
    BaseMCOModel,
    BaseMCO,
    BaseMCOFactory,
    BaseMCOParameter,
    BaseMCOParameterFactory,
    BaseMCOCommunicator,
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

    def run(self, evaluator):
        self.run_called = True
        return self.run_function(evaluator)


class ProbeParameter(BaseMCOParameter):

    test_trait = Int(13, desc="Test trait", verify=True, transient=True)


class ProbeParameterFactory(BaseMCOParameterFactory):
    def get_name(self):
        return "Probe parameter"

    def get_identifier(self):
        return "probe_mco_parameter"

    def get_description(self):
        return "Probe parameter"

    def get_model_class(self):
        return ProbeParameter


class ProbeMCOCommunicator(BaseMCOCommunicator):
    send_called = Bool(False)
    receive_called = Bool(False)

    nb_output_data_values = Int(1)

    def send_to_mco(self, model, kpi_results):
        self.send_called = True

    def receive_from_mco(self, model):
        self.receive_called = True
        return [
            DataValue(name="whatever", value=1.0)
            for _ in range(self.nb_output_data_values)
        ]


class ProbeMCOFactory(BaseMCOFactory):
    nb_output_data_values = Int(1)

    raises_on_create_model = Bool(False)
    raises_on_create_optimizer = Bool(False)
    raises_on_create_communicator = Bool(False)

    optimizer = Any()

    def __init__(self, *args, **kwargs):
        super(ProbeMCOFactory, self).__init__(*args, **kwargs)
        self.optimizer = self.optimizer_class(self)

    def get_identifier(self):
        return "probe_mco"

    def get_model_class(self):
        return ProbeMCOModel

    def get_communicator_class(self):
        return ProbeMCOCommunicator

    def get_optimizer_class(self):
        return ProbeMCO

    def get_name(self):
        return "testmco"

    def create_communicator(self):
        if self.raises_on_create_communicator:
            raise Exception("ProbeMCOFactory.create_communicator")

        return self.communicator_class(
            self, nb_output_data_values=self.nb_output_data_values
        )

    def create_model(self, model_data=None):
        if self.raises_on_create_model:
            raise Exception("ProbeMCOFactory.create_model")

        if model_data is None:
            model_data = {}

        return self.model_class(self, **model_data)

    def create_optimizer(self):
        if self.raises_on_create_optimizer:
            raise Exception("ProbeMCOFactory.create_optimizer")

        return self.optimizer

    def get_parameter_factory_classes(self):
        return [ProbeParameterFactory]
