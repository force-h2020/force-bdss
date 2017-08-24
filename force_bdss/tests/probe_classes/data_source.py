from traits.api import Bool, Function, Str, Int, on_trait_change, Type

from force_bdss.api import (
    BaseDataSourceFactory, BaseDataSourceModel, BaseDataSource,
    Slot
)

from .evaluator_factory import ProbeEvaluatorFactory


class ProbeDataSource(BaseDataSource):
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


class ProbeDataSourceModel(BaseDataSourceModel):
    input_slots_type = Str('PRESSURE')
    output_slots_type = Str('PRESSURE')

    input_slots_size = Int(0)
    output_slots_size = Int(0)

    @on_trait_change('input_slots_type,output_slots_type,'
                     'input_slots_size,output_slots_size')
    def update_slots(self):
        self.changes_slots = True


class ProbeDataSourceFactory(BaseDataSourceFactory,
                             ProbeEvaluatorFactory):
    id = Str('enthought.test.data_source')
    name = Str('test_data_source')

    model_class = Type(ProbeDataSourceModel)

    def create_model(self, model_data=None):
        return self.model_class(
            factory=self,
            input_slots_type=self.input_slots_type,
            output_slots_type=self.output_slots_type,
            input_slots_size=self.input_slots_size,
            output_slots_size=self.output_slots_size,
            **model_data
        )

    def create_data_source(self):
        return ProbeDataSource(
            factory=self,
            run_function=self.run_function,
        )
