from __future__ import print_function

import sys
import logging

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

        mco_data_values = self._get_data_values_from_mco(mco_model,
                                                         mco_communicator)

        ds_results = self._compute_ds_results(
            mco_data_values,
            workflow)

        kpi_results = self._compute_kpi_results(
            ds_results + mco_data_values,
            workflow)

        mco_communicator.send_to_mco(mco_model, kpi_results)

    def _compute_ds_results(self, environment_data_values, workflow):
        """Helper routine.
        Performs the evaluation of the DataSources, passing the current
        environment data values (the MCO data)
        """
        ds_results = []

        for ds_model in workflow.data_sources:
            ds_bundle = ds_model.bundle
            data_source = ds_bundle.create_data_source()

            # Get the slots for this data source. These must be matched to
            # the appropriate values in the environment data values.
            # Matching is by position.
            in_slots, out_slots = data_source.slots(ds_model)

            # Binding performs the extraction of the specified data values
            # satisfying the above input slots from the environment data values
            # considering what the user specified in terms of names (which is
            # in the model input slot maps.
            # The resulting data are the ones picked by name from the
            # environment data values, and in the appropriate ordering as
            # needed by the input slots.
            passed_data_values = self._bind_data_values(
                environment_data_values,
                ds_model.input_slot_maps,
                in_slots)

            # execute data source, passing only relevant data values.
            logging.info("Evaluating for Data Source {}".format(
                ds_bundle.name))
            res = data_source.run(ds_model, passed_data_values)

            if len(res) != len(out_slots):
                error_txt = (
                    "The number of data values ({} values) returned"
                    " by the DataSource '{}' does not match the number"
                    " of output slots it specifies ({} values)."
                    " This is likely a DataSource plugin error.").format(
                    len(res), ds_bundle.name, len(out_slots)
                )

                logging.error(error_txt)
                raise RuntimeError(error_txt)

            if len(res) != len(ds_model.output_slot_names):
                error_txt = (
                    "The number of data values ({} values) returned"
                    " by the DataSource '{}' does not match the number"
                    " of user-defined names specified ({} values)."
                    " This is likely a DataSource plugin error.").format(
                    len(res),
                    ds_bundle.name,
                    len(ds_model.output_slot_names)
                )

                logging.error(error_txt)
                raise RuntimeError(error_txt)

            # At this point, the returned data values are unnamed.
            # Add the names as specified by the user.
            for dv, output_slot_name in zip(res, ds_model.output_slot_names):
                dv.name = output_slot_name

            ds_results.extend(res)

        # Finally, return all the computed data values from all data sources,
        # properly named.
        return ds_results

    def _compute_kpi_results(self, environment_data_values, workflow):
        """Perform evaluation of all KPI calculators.
        environment_data_values contains all data values provided from
        the MCO and data sources.
        """
        kpi_results = []

        for kpic_model in workflow.kpi_calculators:
            kpic_bundle = kpic_model.bundle
            kpi_calculator = kpic_bundle.create_kpi_calculator()

            in_slots, out_slots = kpi_calculator.slots(kpic_model)

            passed_data_values = self._bind_data_values(
                environment_data_values,
                kpic_model.input_slot_maps,
                in_slots)

            logging.info("Evaluating for KPICalculator {}".format(
                kpic_bundle.name))

            res = kpi_calculator.run(kpic_model, passed_data_values)

            if len(res) != len(out_slots):
                error_txt = (
                    "The number of data values ({} values) returned by"
                    " the KPICalculator '{}' does not match the"
                    " number of output slots ({} values). This is"
                    " likely a KPICalculator plugin error."
                ).format(len(res), kpic_bundle.name, len(out_slots))
                logging.error(error_txt)
                raise RuntimeError(error_txt)

            if len(res) != len(kpic_model.output_slot_names):
                error_txt = (
                    "The number of data values ({} values) returned by"
                    " the KPICalculator '{}' does not match the"
                    " number of user-defined names specified ({} values)."
                    " This is either an input file error or a plugin"
                    " error."
                ).format(len(res), kpic_bundle.name,
                         len(kpic_model.output_slot_names))
                logging.error(error_txt)
                raise RuntimeError(error_txt)

            for kpi, output_slot_name in zip(
                    res, kpic_model.output_slot_names):
                kpi.name = output_slot_name

            kpi_results.extend(res)

        return kpi_results

    def _get_data_values_from_mco(self, model, communicator):
        """Helper method.
        Receives the data (in order) from the MCO, and bind them to the
        specified names as from the model.

        Parameters
        ----------
        model: BaseMCOModel
            the MCO model (where the user-defined variable names are specified)
        communicator: BaseMCOCommunicator
            The communicator that produces the (temporarily unnamed) datavalues
            from the MCO.
        """
        mco_data_values = communicator.receive_from_mco(model)

        if len(mco_data_values) != len(model.parameters):
            error_txt = ("The number of data values returned by"
                         " the MCO ({} values) does not match the"
                         " number of parameters specified ({} values)."
                         " This is either a MCO plugin error or the workflow"
                         " file is corrupted.").format(
                len(mco_data_values), len(model.parameters)
            )
            logging.error(error_txt)
            raise RuntimeError(error_txt)

        # The data values obtained by the communicator are unnamed.
        # Assign the name to each datavalue as specified by the user.
        for dv, param in zip(mco_data_values, model.parameters):
            dv.name = param.name

        return mco_data_values

    def _bind_data_values(self,
                          available_data_values,
                          model_slot_map,
                          slots):
        """
        Given the named data values in the environment, the slots a given
        data source expects, and the user-specified names for each of these
        slots, returns those data values with the requested names, ordered
        in the correct order as specified by the slot map.
        """
        passed_data_values = []
        lookup_map = {dv.name: dv for dv in available_data_values}

        if len(slots) > len(model_slot_map):
            raise RuntimeError("The length of the slots is greater than"
                               " the length of the slot map. This may"
                               " indicate a file error")

        for slot, slot_map in zip(slots, model_slot_map):
            passed_data_values.append(lookup_map[slot_map.name])

        return passed_data_values
