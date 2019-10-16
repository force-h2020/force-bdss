import logging

from traits.api import (
    HasStrictTraits, Instance, Unicode, provides,
    DelegatesTo
)

from force_bdss.core.data_value import DataValue
from force_bdss.core.workflow import Workflow
from force_bdss.mco.i_evaluator import IEvaluator

log = logging.getLogger(__name__)


@provides(IEvaluator)
class WorkflowEvaluator(HasStrictTraits):
    """A class that can be passed into a BaseMCO to evaluate the
    state of a system described by a Workflow object a given set of
    parameter values."""

    #: The workflow instance.
    workflow = Instance(Workflow)

    #: A reference to the mco model of the workflow instance.
    mco_model = DelegatesTo('workflow', prefix='mco')

    #: The path to the workflow file.
    workflow_filepath = Unicode()

    def _internal_evaluate(self, parameter_values):
        """Evaluates the workflow using the given parameter values
        running on the internal process"""

        data_values = [
            DataValue(type=parameter.type,
                      name=parameter.name,
                      value=value)
            for parameter, value in zip(
                self.mco_model.parameters, parameter_values)]

        kpi_results = self.workflow.execute(data_values)

        # Return just the values to the MCO, since the DataValue
        # class is not specific to the BaseMCO classes
        kpi_values = [kpi.value for kpi in kpi_results]

        return kpi_values

    def evaluate(self, parameter_values):
        """Public method to evaluate the workflow at a given set of
        MCO parameter values

        Parameters
        ----------
        parameter_values: list
            List of values to assign to each BaseMCOParameter defined
            in the workflow

        Returns
        -------
        kpi_results: list
            List of values corresponding to each MCO KPI in the
            workflow
        """
        return self._internal_evaluate(parameter_values)
