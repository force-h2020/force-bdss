import logging
from traits.api import HasStrictTraits, Str, Any

logger = logging.getLogger(__name__)


class VerifierError(HasStrictTraits):
    subject = Any()
    error = Str()


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
                error="Workflow has no MCO"
            )
        )
        return errors

    mco = workflow.mco
    if len(mco.parameters) == 0:
        errors.append(VerifierError(subject=mco,
                                    error="MCO has no defined parameters"))

    for idx, param in enumerate(mco.parameters):
        if len(param.name.strip()) == 0:
            errors.append(VerifierError(subject=param,
                                        error="Parameter {} "
                                              "has empty name".format(idx)))
        if len(param.type.strip()) == 0:
            errors.append(VerifierError(subject=param,
                                        error="Parameter {} "
                                              "has empty type".format(idx)))

    for idx, kpi in enumerate(mco.kpis):
        if len(kpi.name.strip()) == 0:
            errors.append(VerifierError(subject=kpi,
                                        error="KPI {} has empty name".format(
                                            idx)))
        if len(kpi.objective.strip()) == 0:
            errors.append(VerifierError(subject=kpi,
                                        error="KPI {} has empty "
                                              "objective".format(idx)))

    return errors


def _check_execution_layers(workflow):
    errors = []

    layers = workflow.execution_layers
    if len(layers) == 0:
        errors.append(
            VerifierError(
                subject=workflow,
                error="Workflow has no execution layers"
            )
        )

        return errors

    for idx, layer in enumerate(layers):
        if len(layer.data_sources) == 0:
            errors.append(VerifierError(subject=layer,
                                        error="Layer {} has no "
                                              "data sources".format(idx)))

        for ds in layer.data_sources:
            errors.extend(_check_data_source(ds, idx))

    return errors


def _check_data_source(data_source_model, layer_no):
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
            error="Missing input slot name assignment "
                  "in layer {}".format(layer_no)))

    for idx, info in enumerate(data_source_model.input_slot_info):
        if len(info.name.strip()) == 0:
            errors.append(VerifierError(
                subject=data_source_model,
                error="Undefined name for input "
                      "parameter {} in layer {}".format(idx, layer_no)))

    if len(output_slots) != len(data_source_model.output_slot_info):
        errors.append(VerifierError(
            subject=data_source_model,
            error="Missing output slot name assignment "
                  "in layer {}".format(layer_no)))

    for idx, info in enumerate(data_source_model.output_slot_info):
        if len(info.name.strip()) == 0:
            errors.append(VerifierError(
                subject=data_source_model,
                error="Undefined name for output "
                      "parameter {} in layer {}".format(idx, layer_no)))

    return errors
