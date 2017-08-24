try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin

from traits.api import (HasStrictTraits, Bool, Function, Str, Int,
                        on_trait_change)

from force_bdss.api import (
    BaseKPICalculatorFactory, BaseKPICalculatorModel, BaseKPICalculator,
    Slot
)


class ProbeEvaluator(BaseKPICalculator):
    run_function = Function

    run_called = Bool(False)
    slots_called = Bool(False)

    def run(self, model, parameters):
        self.run_called = True
        self.run_function(model, parameters)

    def slots(self, model):
        self.slots_called = True
        return (
            tuple(Slot(type=model.input_slots_type)
                  for _ in range(model.input_slots_size))
        ), (
            tuple(Slot(type=model.output_slots_type)
                  for _ in range(model.output_slots_size))
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


class ProbeKPICalculatorModel(BaseKPICalculatorModel):
    input_slots_type = Str('PRESSURE')
    output_slots_type = Str('PRESSURE')

    input_slots_size = Int(0)
    output_slots_size = Int(0)

    @on_trait_change('input_slots_type,output_slots_type,'
                     'input_slots_size,output_slots_size')
    def update_slots(self):
        self.changes_slots = True


class ProbeKPICalculatorFactory(BaseKPICalculatorFactory,
                                ProbeEvaluatorFactory):
    id = Str('enthought.test.kpi_calculator')
    name = Str('test_kpi_calculator')

    model_class = ProbeKPICalculatorModel

    def create_model(self, model_data=None):
        return self.model_class(
            factory=self,
            input_slots_type=self.input_slots_type,
            output_slots_type=self.output_slots_type,
            input_slots_size=self.input_slots_size,
            output_slots_size=self.output_slots_size,
            **model_data
        )

    def create_kpi_calculator(self):
        return ProbeEvaluator(
            factory=self,
            run_function=self.run_function,
        )
