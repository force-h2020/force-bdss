#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Bool, Function, Int, on_trait_change

from force_bdss.core.data_value import DataValue
from force_bdss.core.slot import Slot
from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.data_sources.base_data_source_factory import (
    BaseDataSourceFactory,
)
from force_bdss.local_traits import CUBAType


def run_func(model, parameters):
    return [DataValue() for _ in range(model.output_slots_size)]


def raise_exception(*args, **kwargs):
    raise Exception()


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
            (
                tuple(
                    Slot(type=model.input_slots_type)
                    for _ in range(model.input_slots_size)
                )
            ),
            (
                tuple(
                    Slot(type=model.output_slots_type)
                    for _ in range(model.output_slots_size)
                )
            ),
        )


class ProbeDataSourceModel(BaseDataSourceModel):
    input_slots_type = CUBAType("PRESSURE")
    output_slots_type = CUBAType("PRESSURE")

    input_slots_size = Int(1)
    output_slots_size = Int(1)

    test_trait = Int(13, desc="Test trait", verify=True, transient=True)

    @on_trait_change(
        "input_slots_type,output_slots_type,"
        "input_slots_size,output_slots_size"
    )
    def update_slots(self):
        self.changes_slots = True


class ProbeDataSourceFactory(BaseDataSourceFactory):

    run_function = Function(default_value=run_func)

    input_slots_type = CUBAType("PRESSURE")
    output_slots_type = CUBAType("PRESSURE")

    input_slots_size = Int(1)
    output_slots_size = Int(1)

    raises_on_create_model = Bool(False)
    raises_on_create_data_source = Bool(False)

    raises_on_data_source_run = Bool(False)

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

        if self.raises_on_data_source_run:
            run_function = raise_exception
        else:
            run_function = self.run_function

        return self.data_source_class(factory=self, run_function=run_function)
