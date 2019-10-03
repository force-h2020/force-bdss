import logging

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
    available_data_values = workflow.mco.bind_parameters(data_values)

    for index, layer in enumerate(workflow.execution_layers):
        log.info("Computing data layer {}".format(index))
        ds_results = layer.execute_layer(available_data_values)
        available_data_values += ds_results

    log.info("Aggregating KPI data")

    kpi_results = workflow.mco.bind_kpis(ds_results)

    return kpi_results
