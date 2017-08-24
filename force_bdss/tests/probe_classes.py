try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin

from traits.api import HasStrictTraits, Bool, Function, Str, Int, Dict

from force_bdss.api import (
    BaseKPICalculatorFactory, BaseKPICalculatorModel, BaseKPICalculator,
    Slot
)


class ProbeEvaluator(HasStrictTraits):
    run_function = Function

    input_slots_type = Str('PRESSURE')
    output_slots_type = Str('PRESSURE')

    input_slots_size = Int(0)
    output_slots_size = Int(0)

    run_called = Bool(False)
    slots_called = Bool(False)

    def run(self, model, parameters):
        self.run_called = True
        self.run_function(model, parameters)

    def slots(self, model):
        self.slots_called = True
        return (
            tuple(Slot(type=self.input_slots_type)
                  for _ in range(self.input_slots_size))
        ), (
            tuple(Slot(type=self.output_slots_type)
                  for _ in range(self.output_slots_size))
        )


class ProbeEvaluatorFactory(HasStrictTraits):
    def __init__(self, plugin=None, *args, **kwargs):
        if plugin is None:
            plugin = mock.Mock(Plugin)

        super(ProbeEvaluatorFactory, self).__init__(
            plugin=plugin, *args, **kwargs)

    run_function = Function

    input_slots_type = Str('PRESSURE')
    output_slots_type = Str('PRESSURE')

    input_slots_size = Int(0)
    output_slots_size = Int(0)

    model_data = Dict()


class ProbeKPICalculator(BaseKPICalculator, ProbeEvaluator):
    pass


class ProbeKPICalculatorModel(BaseKPICalculatorModel):
    def __init__(self, factory, model_data, *args, **kwargs):
        for key, value in model_data.items():
            setattr(self, key, value)

        super(ProbeKPICalculatorModel, self).__init__(
            self, factory, *args, **kwargs)


class ProbeKPICalculatorFactory(BaseKPICalculatorFactory,
                                ProbeEvaluatorFactory):
    id = Str('enthought.test.datasource')
    name = Str('test_datasource')

    def create_model(self, model_data=None):
        return ProbeKPICalculatorModel(self, self.model_data)

    def create_kpi_calculator(self):
        return ProbeKPICalculator(
            factory=self,
            run_function=self.run_function,
            input_slots_type=self.input_slots_type,
            output_slots_type=self.output_slots_type,
            input_slots_size=self.input_slots_size,
            output_slots_size=self.output_slots_size
        )
