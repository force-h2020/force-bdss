import logging
from force_bdss.core.data_value import DataValue

log = logging.getLogger(__name__)


def execute_workflow(workflow, data_values):
    """Executes the given workflow using the list of data values.
    Returns a list of data values for the KPI results

    Parameters
    ----------
    workflow: Workflow
        The instance of the workflow

    data_values: List
        The data values that the MCO generally provides.

    Returns
    -------
    list: A list of DataValues containing the KPI results.
    """

    available_data_values = data_values[:]
    for index, layer in enumerate(workflow.execution_layers):
        log.info("Computing data layer {}".format(index))
        ds_results = execute_layer(layer, available_data_values)
        available_data_values += ds_results

    log.info("Aggregating KPI data")

    kpi_results = []
    kpi_names = [kpi.name for kpi in workflow.mco.kpis]

    kpi_results = [
        dv
        for kpi_name in kpi_names
        for dv in available_data_values
        if dv.name == kpi_name
    ]

    return kpi_results


def execute_layer(layer, environment_data_values):
    """Helper routine.
    Performs the evaluation of a single layer.
    At the moment we have a single layer of DataSources followed
    by a single layer of KPI calculators.

    Parameters
    ----------
    layer: ExecutionLayer
        A list of the models for all the data sources

    environment_data_values: list
        A list of data values to submit to the evaluators.

    NOTE: The above parameter is going to go away as soon as we move
    to unlimited layers and remove the distinction between data sources
    and KPI calculators.
    """
    results = []

    for model in layer.data_sources:
        factory = model.factory

        # Create an instance of the data source contained in the factory
        data_source = factory.create_data_source()

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
