import logging

from itertools import groupby

from traits.api import HasStrictTraits, Unicode, Any

logger = logging.getLogger(__name__)


class VerifierError(HasStrictTraits):
    subject = Any()
    #: An error message relevant to the local modelview
    local_error = Unicode()
    #: An error message relevant to the overall workflow
    global_error = Unicode()

    def __init__(self, subject, global_error='', local_error=''):
        if local_error == '':
            local_error = global_error

        super(VerifierError, self).__init__(
            subject=subject,
            global_error=global_error,
            local_error=local_error
        )


def verify_workflow(workflow):
    """Verifies if the workflow can be executed, and specifies where the
    error occurs and why.

    """
    result = []
    result.extend(_check_mco(workflow))
    result.extend(_check_execution_layers(workflow))
    return result


def _check_mco(workflow):
    errors = []
    if workflow.mco is None:
        errors.append(
            VerifierError(
                subject=workflow,
                local_error="Workflow has no MCO",
            )
        )
        return errors

    mco = workflow.mco
    if len(mco.parameters) == 0:
        errors.append(VerifierError(
            subject=mco,
            global_error="The MCO has no defined parameters"))

    #: Check MCO parameters have names and types
    for idx, param in enumerate(mco.parameters):
        factory_name = param.factory.name
        if param.name == '':
            errors.append(VerifierError(
                subject=param,
                local_error="MCO parameter is not named",
                global_error="Error in MCO parameter "
                             "(Type: {})".format(factory_name)))

        if len(param.type.strip()) == 0:
            errors.append(VerifierError(
                subject=param,
                local_error="MCO parameter has no type set",
                global_error="Error in MCO parameter "
                             "(Type: {})".format(factory_name)))

    #: Check KPIs have names and optimisation objectives
    for idx, kpi in enumerate(mco.kpis):
        if kpi.name == '':
            errors.append(VerifierError(subject=kpi,
                                        local_error="KPI is not named",
                                        global_error="A KPI has an error"))
        if kpi.objective == '':
            errors.append(VerifierError(subject=kpi,
                                        local_error="KPI has no objective set",
                                        global_error="A KPI has an error"))

    return errors


def _check_execution_layers(workflow):
    errors = []

    layers = workflow.execution_layers
    if len(layers) == 0:
        errors.append(
            VerifierError(
                subject=workflow,
                global_error="Workflow has no execution layers"
            )
        )

        return errors

    layer_index_errors = []
    for idx, layer in enumerate(layers):
        if len(layer.data_sources) == 0:
            layer_index_errors.append(idx)
            errors.append(VerifierError(
                subject=layer, local_error="Layer has no data sources"))

        for ds in layer.data_sources:
            errors.extend(_check_data_source(ds, idx))

    if layer_index_errors != []:
        multi_str = multi_error_format(layer_index_errors)
        if len(layer_index_errors) == 1:
            errors.append(VerifierError(
                subject=workflow,
                local_error="Layer {} has no data sources".format(multi_str)))
        else:
            errors.append(VerifierError(
                subject=workflow,
                local_error="Layers {} have no data "
                            "sources".format(multi_str)))

    return errors


def _check_data_source(data_source_model, layer_number):
    errors = []

    factory = data_source_model.factory
    try:
        data_source = factory.create_data_source()
    except Exception:
        logger.exception("Unable to create data source from factory"
                         " '{}', plugin '{}'. This might indicate a "
                         "programming error".format(factory.id,
                                                    factory.plugin.id))
        raise

    try:
        input_slots, output_slots = data_source.slots(data_source_model)
    except Exception:
        logger.exception(
            "Unable to retrieve slot information from data source"
            " created by factory '{}', plugin '{}'. This might "
            "indicate a programming error.".format(
                data_source.factory.id,
                data_source.factory.plugin.id))
        raise

    if len(input_slots) != len(data_source_model.input_slot_info):
        errors.append(VerifierError(
            subject=data_source_model,
            global_error="Missing input slot name assignment "
                         "in layer {}".format(layer_number)))

    #: Check if any input slots are unnamed
    row_index_errors = []
    for idx, info in enumerate(data_source_model.input_slot_info):
        if info.name == '':
            row_index_errors.append(idx)

    if row_index_errors != []:
        err_no_string = multi_error_format(row_index_errors)
        if len(row_index_errors) == 1:
            errors.append(VerifierError(
                subject=data_source_model,
                local_error="Undefined name for input parameter "
                            "{}".format(err_no_string),
                global_error="An input parameter is undefined in {} "
                             "(Layer {})".format(factory.name, layer_number)))
        else:
            errors.append(VerifierError(
                subject=data_source_model,
                local_error="Undefined name for input parameters "
                            "{}".format(err_no_string),
                global_error="An input parameter is undefined in {} "
                             "(Layer {})".format(factory.name, layer_number)))

    if len(output_slots) != len(data_source_model.output_slot_info):
        errors.append(VerifierError(
            subject=data_source_model,
            global_error="Missing output slot name assignment "
                         "in layer {}".format(layer_number)))

    #: Check if the datasource has all outputs unnamed
    unnamed = [info.name == "" for info in data_source_model.output_slot_info]
    if all(unnamed) and len(unnamed) != 0:
        errors.append(VerifierError(
            subject=data_source_model,
            local_error="Undefined names for all output "
                        "parameters",
            global_error="An output parameter is undefined in {}"
                         " (Layer {})".format(factory.name, layer_number)))

    return errors


def multi_error_format(index_list):
    """Takes a list of integers and returns a string where they are grouped
    consecutively wherever possible.
    For example an input of [0,1,2,4,5,7] returns the string '0-2, 4-5, 7' """
    index_list.sort()
    # Single, consecutive or non-consecutive
    if len(index_list) == 1:
        return str(index_list[0])
    else:
        repl = []

        for i, index_group in groupby(enumerate(index_list), lambda val:
                                      val[0]-val[1]):
            group_index_list = []
            for enum_idx, error_idx in index_group:
                group_index_list.append(error_idx)
            if len(group_index_list) == 1:
                repl.append(str(group_index_list[0]))
            else:
                repl.append('{}-{}'.format(group_index_list[0],
                                           group_index_list[-1]))
        # Conversion from list of strings to comma separated string
        return_string = ', '.join(repl)

    return return_string
