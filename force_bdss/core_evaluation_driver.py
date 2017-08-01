from __future__ import print_function

import sys
from traits.api import on_trait_change

from .ids import plugin_id
from .base_core_driver import BaseCoreDriver
from .io.workflow_reader import (
    InvalidVersionException,
    InvalidFileException
)

CORE_EVALUATION_DRIVER_ID = plugin_id("core", "CoreEvaluationDriver")


class CoreEvaluationDriver(BaseCoreDriver):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """
    id = CORE_EVALUATION_DRIVER_ID

    @on_trait_change("application:started")
    def application_started(self):
        try:
            workflow = self.workflow
        except (InvalidVersionException, InvalidFileException) as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        mco_model = workflow.mco
        mco_bundle = mco_model.bundle
        mco_communicator = mco_bundle.create_communicator()

        # Receives the data from the MCO. These are technically unnamed.
        # The names are then assigned. Order is important
        mco_data_values = mco_communicator.receive_from_mco(mco_model)

        if len(mco_data_values) != len(mco_model.parameters):
            raise RuntimeError("The number of data values returned by"
                               " the MCO does not match the number of"
                               " parameters specified. This is likely a"
                               " MCO plugin error.")

        # Assign the name to the data value that was emitted.
        for dv, param in zip(mco_data_values, mco_model.parameters):
            dv.name = param.name

        ds_results = []
        for ds_model in workflow.data_sources:
            ds_bundle = ds_model.bundle
            data_source = ds_bundle.create_data_source()

            in_slots, out_slots = data_source.slots(ds_model)
            passed_data_values = self._bind_data_values(
                mco_data_values,
                ds_model.input_slot_maps,
                in_slots)

            res = data_source.run(ds_model, passed_data_values)
            if len(res) != len(out_slots):
                raise RuntimeError("The number of data values returned by"
                                   " the DataSource does not match the number"
                                   " of parameters specified. This is likely a"
                                   " DataSource plugin error.")

            if len(res) != len(ds_model.output_slot_names):
                raise RuntimeError("The number of data values returned by"
                                   " the DataSource does not match the number"
                                   " of names specified. This is either an"
                                   " input file error or a plugin error.")

            for dv, output_slot_name in zip(res, ds_model.output_slot_names):
                dv.name = output_slot_name

            ds_results.extend(res)

        kpi_results = []
        for kpic_model in workflow.kpi_calculators:
            kpic_bundle = kpic_model.bundle
            kpi_calculator = kpic_bundle.create_kpi_calculator()
            in_slots, out_slots = kpi_calculator.slots(kpic_model)

            passed_data_values = self._bind_data_values(
                mco_data_values+ds_results,
                kpic_model.input_slot_maps,
                in_slots)

            res = kpi_calculator.run(kpic_model, passed_data_values)
            if len(res) != len(out_slots):
                raise RuntimeError("The number of data values returned by"
                                   " the KPICalculator does not match the"
                                   " number of parameters specified. This is"
                                   " likely a KPICalculator plugin error.")

            if len(res) != len(kpic_model.output_slot_names):
                raise RuntimeError("The number of data values returned by"
                                   " the KPICalculator does not match the"
                                   " number of names specified. This is"
                                   " either an input file error or a plugin"
                                   " error.")

            for kpi, output_slot_name in zip(res,
                                             kpic_model.output_slot_names):
                kpi.name = output_slot_name

            kpi_results.extend(res)

        mco_communicator.send_to_mco(mco_model, kpi_results)

    def _bind_data_values(self,
                          available_data_values,
                          model_slot_map,
                          slots):

        passed_data_values = []
        lookup_map = {dv.name: dv for dv in available_data_values}

        if len(slots) > len(model_slot_map):
            raise RuntimeError("The length of the slots is greater than"
                               " the length of the slot map. This may"
                               " indicate a file error")

        for slot, slot_map in zip(slots, model_slot_map):
            passed_data_values.append(lookup_map[slot_map.name])

        return passed_data_values
