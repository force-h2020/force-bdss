import sys
import logging

from traits.api import on_trait_change

from force_bdss.ids import InternalPluginID
from .base_core_driver import BaseCoreDriver


log = logging.getLogger(__name__)


class CoreEvaluationDriver(BaseCoreDriver):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """
    id = InternalPluginID.CORE_EVALUATION_DRIVER_ID

    @on_trait_change("application:started")
    def application_started(self):
        try:
            workflow = self.workflow
        except Exception:
            log.exception("Unable to open workflow file.")
            sys.exit(1)

        mco_model = workflow.mco
        if mco_model is None:
            log.info("No MCO defined. Nothing to do. Exiting.")
            sys.exit(0)

        mco_factory = mco_model.factory
        log.info("Creating communicator")
        try:
            mco_communicator = mco_factory.create_communicator()
        except Exception:
            log.exception(
                "Unable to create communicator from MCO factory '{}' "
                "in plugin '{}'. This may indicate a programming "
                "error in the plugin".format(
                    mco_factory.id,
                    mco_factory.plugin.id))
            raise

        mco_data_values = _get_data_values_from_mco(
            mco_model, mco_communicator)

        kpi_results = execute_workflow(workflow, mco_data_values)

        mco_communicator.send_to_mco(mco_model, kpi_results)


def execute_workflow(workflow, data_values):
    """Executes the given workflow using the list of data values.
    Returns a list of data values for the KPI results
    """

    available_data_values = data_values[:]
    for index, layer in enumerate(workflow.execution_layers):
        log.info("Computing data layer {}".format(index))
        ds_results = _compute_layer_results(
            available_data_values,
            layer,
        )
        available_data_values += ds_results

    log.info("Aggregating KPI data")

    kpi_results = []
    kpi_names = [kpi.name for kpi in workflow.mco.kpis]

    kpi_results = [
        dv
        for dv in available_data_values
        if dv.name in kpi_names
    ]

    return kpi_results


def _compute_layer_results(environment_data_values,
                           layer,
                           ):
    """Helper routine.
    Performs the evaluation of a single layer.
    At the moment we have a single layer of DataSources followed
    by a single layer of KPI calculators.

    Parameters
    ----------
    environment_data_values: list
        A list of data values to submit to the evaluators.

    layer: ExecutionLayer
        A list of the models for all the data sources

    NOTE: The above parameter is going to go away as soon as we move
    to unlimited layers and remove the distinction between data sources
    and KPI calculators.
    """
    results = []

    for model in layer.data_sources:
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

        # Get the slots for this data source. These must be matched to
        # the appropriate values in the environment data values.
        # Matching is by position.
        in_slots, out_slots = data_source.slots(model)

        # Binding performs the extraction of the specified data values
        # satisfying the above input slots from the environment data values
        # considering what the user specified in terms of names (which is
        # in the model input slot info
        # The resulting data are the ones picked by name from the
        # environment data values, and in the appropriate ordering as
        # needed by the input slots.
        passed_data_values = _bind_data_values(
            environment_data_values,
            model.input_slot_info,
            in_slots)

        # execute data source, passing only relevant data values.
        log.info("Evaluating for Data Source {}".format(
            factory.name))
        log.info("Passed values:")
        for idx, dv in enumerate(passed_data_values):
            log.info("{}: {}".format(idx, dv))

        try:
            res = data_source.run(model, passed_data_values)
        except Exception:
            log.exception(
                "Evaluation could not be performed. "
                "Run method raised exception.")
            raise

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

        # At this point, the returned data values are unnamed.
        # Add the names as specified by the user.
        for dv, output_slot_info in zip(res, model.output_slot_info):
            dv.name = output_slot_info.name

        # If the name was not specified, simply discard the value,
        # because apparently the user is not interested in it.
        res = [r for r in res if r.name != ""]
        results.extend(res)

        log.info("Returned values:")
        for idx, dv in enumerate(res):
            log.info("{}: {}".format(idx, dv))

    # Finally, return all the computed data values from all evaluators,
    # properly named.
    return results


def _get_data_values_from_mco(model, communicator):
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

    log.info("Received data from MCO: \n{}".format(
             "\n".join([str(x) for x in mco_data_values])))

    if len(mco_data_values) != len(model.parameters):
        error_txt = ("The number of data values returned by"
                     " the MCO ({} values) does not match the"
                     " number of parameters specified ({} values)."
                     " This is either a MCO plugin error or the workflow"
                     " file is corrupted.").format(
            len(mco_data_values), len(model.parameters)
        )
        log.error(error_txt)
        raise RuntimeError(error_txt)

    # The data values obtained by the communicator are unnamed.
    # Assign the name to each datavalue as specified by the user.
    for dv, param in zip(mco_data_values, model.parameters):
        dv.name = param.name

    # Exclude those who have no name set.
    return [dv for dv in mco_data_values if dv.name != ""]


def _bind_data_values(available_data_values,
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

    if len(slots) != len(model_slot_map):
        raise RuntimeError("The length of the slots is not equal to"
                           " the length of the slot map. This may"
                           " indicate a file error.")

    try:
        for slot, slot_map in zip(slots, model_slot_map):
            passed_data_values.append(lookup_map[slot_map.name])
    except KeyError:
        raise RuntimeError(
            "Unable to find requested name '{}' in available "
            "data values. Current data value names: {}".format(
                slot_map.name,
                list(lookup_map.keys())))

    return passed_data_values
