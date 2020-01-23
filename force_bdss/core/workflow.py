import logging

from traits.api import HasStrictTraits, Instance, List, provides

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.verifier import VerifierError
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.notification_listeners.base_notification_listener_model \
    import BaseNotificationListenerModel
from force_bdss.mco.i_evaluator import IEvaluator
from force_bdss.core.data_value import DataValue


log = logging.getLogger(__name__)


class WorkflowAttributeWarning:
    warning_message = (
        "The Workflow object format with 'mco' attribute is now"
        " deprecated. Please use 'mco_model' attribute instead."
    )

    @classmethod
    def warn(cls):
        log.warning(cls.warning_message)


@provides(IEvaluator)
class Workflow(HasStrictTraits):
    """Model object that represents the Workflow as a whole"""

    #: The Workflow MCOModel object.
    #: Can be None if no MCOModel has been specified yet.
    mco_model = Instance(BaseMCOModel, allow_none=True)

    #: The execution layers. Execution starts from the first layer,
    #: where all data sources are executed in sequence. It then passes all
    #: the computed data to the second layer, then the third etc.
    execution_layers = List(ExecutionLayer)

    #: Contains information about the listeners to be setup
    notification_listeners = List(BaseNotificationListenerModel)

    def execute(self, data_values):
        """Executes the given workflow using the list of data values.
        Returns a list of data values for the KPI results

        Parameters
        ----------
        data_values : list of DataValue
            The data values that the MCO generally provides.

        Returns
        -------
        kpis : list of DataValues
            The DataValues containing the KPI results.
        """
        available_data_values = self.mco_model.bind_parameters(data_values)

        for index, layer in enumerate(self.execution_layers):
            log.info("Computing data layer {}".format(index))
            ds_results = layer.execute_layer(available_data_values)
            available_data_values += ds_results

        log.info("Aggregating KPI data")
        kpi_results = self.mco_model.bind_kpis(available_data_values)

        return kpi_results

    def verify(self):
        """ Verify the workflow.

        The workflow must have:
        - an MCO
        - at least one execution layer
        - no errors in the MCO or any execution layer

        Returns
        -------
        errors : list of VerifierErrors
            The list of all detected errors in the workflow.
        """
        errors = []

        if not self.mco_model:
            errors.append(
                VerifierError(subject=self, global_error="Workflow has no MCO")
            )
        else:
            errors += self.mco_model.verify()

        if not self.execution_layers:
            errors.append(
                VerifierError(
                    subject=self,
                    global_error="Workflow has no execution layers",
                )
            )
        else:
            for layer in self.execution_layers:
                errors += layer.verify()

        return errors

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

    def _internal_evaluate(self, parameter_values):
        """Evaluates the workflow using the given parameter values
        running on the internal process"""

        data_values = [
            DataValue(type=parameter.type, name=parameter.name, value=value)
            for parameter, value in zip(
                self.mco_model.parameters, parameter_values
            )
        ]

        kpi_results = self.execute(data_values)

        # Return just the values to the MCO, since the DataValue
        # class is not specific to the BaseMCO classes
        kpi_values = [kpi.value for kpi in kpi_results]

        return kpi_values
