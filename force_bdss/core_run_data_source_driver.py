import sys
import logging

from traits.api import on_trait_change, Unicode

from force_bdss.core.data_value import DataValue
from force_bdss.ids import InternalPluginID
from .base_core_driver import BaseCoreDriver


log = logging.getLogger(__name__)


class CoreRunDataSourceDriver(BaseCoreDriver):
    """Main plugin that handles the execution of a single data source"""
    id = InternalPluginID.CORE_RUN_DATASOURCE_DRIVER_ID

    run_data_source = Unicode()

    @on_trait_change("application:started")
    def application_started(self):
        try:
            workflow = self.workflow
        except Exception:
            log.exception("Unable to open workflow file.")
            sys.exit(1)

        model = _find_data_source_model(workflow, self.run_data_source)

        if model is None:
            raise RuntimeError(
                "Unable to find model information for data "
                "source with id {}".format(self.run_data_source))

        factory = model.factory
        try:
            data_source = factory.create_data_source()
        except Exception:
            log.exception(
                "Unable to create data source from factory '{}' "
                "in plugin '{}'. This may indicate a programming "
                "error in the plugin".format(
                    factory.id,
                    factory.plugin.id))
            raise

        in_slots, out_slots = data_source.slots(model)

        print("DataSource: {}".format(factory.id))

        print("Input Slots:")
        for slot in in_slots:
            print("    {}: {}".format(slot.type, slot.description))

        print("Output Slots:")
        for slot in out_slots:
            print("    {}: {}".format(slot.type, slot.description))

        values = []

        if len(in_slots) > 0:
            print("Input values for input slots, separated by spaces:")
            line = sys.stdin.readline().strip()
            if len(line) == 0:
                raise RuntimeError(
                    "Specified input is empty. Please provide values.")

            try:
                values = [float(x) for x in line.split()]
            except ValueError:
                raise RuntimeError(
                    "Unable to convert values to floating point number. "
                    "Please check your input.")

        if len(values) != len(in_slots):
            raise RuntimeError(
                "The number of specified values did not match the number "
                "of slots.")

        # transfer the values to datavalue instances, matching then with the
        # appropriate type from the in_slot.
        data_values = [
            DataValue(type=slot.type, value=value)
            for slot, value in zip(in_slots, values)
        ]

        try:
            res = data_source.run(model, data_values)
        except Exception:
            log.exception(
                "Evaluation could not be performed. "
                "Run method raised exception.")
            raise

        if not isinstance(res, list):
            error_txt = (
                "The run method of data source {} must return a list."
                " It returned instead {}. Fix the run() method to return"
                " the appropriate entity.".format(
                    factory.name,
                    type(res)
                ))
            log.error(error_txt)
            raise RuntimeError(error_txt)

        if len(res) != len(out_slots):
            error_txt = (
                "The number of data values ({} values) returned"
                " by '{}' does not match the number"
                " of output slots it specifies ({} values)."
                " This is likely a plugin error.").format(
                len(res), factory.name, len(out_slots)
            )

            log.error(error_txt)
            raise RuntimeError(error_txt)

        if len(res) != len(model.output_slot_info):
            error_txt = (
                "The number of data values ({} values) returned"
                " by '{}' does not match the number"
                " of user-defined names specified ({} values)."
                " This is either a plugin error or a file"
                " error.").format(
                len(res),
                factory.name,
                len(model.output_slot_info)
            )

            log.error(error_txt)
            raise RuntimeError(error_txt)

        for idx, dv in enumerate(res):
            if not isinstance(dv, DataValue):
                error_txt = (
                    "The result list returned by DataSource {} contains"
                    " an entry that is not a DataValue. An entry of type"
                    " {} was instead found in position {}."
                    " Fix the DataSource.run() method"
                    " to return the appropriate entity.".format(
                        factory.name,
                        type(dv),
                        idx
                    )
                )
                log.error(error_txt)
                raise RuntimeError(error_txt)

        # At this point, the returned data values are unnamed.
        # Add the names as specified by the user.
        for dv, output_slot_info in zip(res, model.output_slot_info):
            dv.name = output_slot_info.name

        print("Result:")
        for idx, dv in enumerate(res):
            print("    {}: {}".format(idx, dv))


def _find_data_source_model(workflow, data_source_id):
    """Finds the data source model on the workflow by data source id.
    The match looks if the passed id is contained in the full id, so a
    substring will also suffice.
    """
    for layer in workflow.execution_layers:
        for data_source_model in layer.data_sources:
            if data_source_id in data_source_model.factory.id:
                return data_source_model

    return None

