from traits.api import Bool, Function, Unicode, Int, on_trait_change

from force_bdss.api import (
    BaseDataSourceFactory, BaseDataSourceModel, BaseDataSource,
    Slot
)
from force_bdss.core.data_value import DataValue


def run_func(model, parameters):
    return [DataValue() for _ in range(model.output_slots_size)]


class ProbeDataSource(BaseDataSource):
    run_function = Function(default_value=run_func)

    run_called = Bool(False)
    slots_called = Bool(False)

    def run(self, model, parameters):
        self.run_called = True
        return self.run_function(model, parameters)

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
    input_slots_type = Unicode('PRESSURE')
    output_slots_type = Unicode('PRESSURE')

    input_slots_size = Int(1)
    output_slots_size = Int(1)

    @on_trait_change('input_slots_type,output_slots_type,'
                     'input_slots_size,output_slots_size')
    def update_slots(self):
        self.changes_slots = True


class ProbeDataSourceFactory(BaseDataSourceFactory):

    run_function = Function(default_value=run_func)

    input_slots_type = Unicode('PRESSURE')
    output_slots_type = Unicode('PRESSURE')

    input_slots_size = Int(1)
    output_slots_size = Int(1)

    raises_on_create_model = Bool(False)
    raises_on_create_data_source = Bool(False)

    def get_identifier(self):
        return "probe_data_source"

    def get_name(self):
        return "test_data_source"

    def get_model_class(self):
        return ProbeDataSourceModel

    def get_data_source_class(self):
        return ProbeDataSource

    def create_model(self, model_data=None):
        if self.raises_on_create_model:
            raise Exception("ProbeDataSourceFactory.create_model")

        if model_data is None:
            model_data = {}
        return self.model_class(
            factory=self,
            input_slots_type=self.input_slots_type,
            output_slots_type=self.output_slots_type,
            input_slots_size=self.input_slots_size,
            output_slots_size=self.output_slots_size,
            **model_data
        )

    def create_data_source(self):
        if self.raises_on_create_data_source:
            raise Exception("ProbeDataSourceFactory.create_data_source")

        return self.data_source_class(
            factory=self,
            run_function=self.run_function,
        )
