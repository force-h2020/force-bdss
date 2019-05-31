import logging

from traits.api import HasStrictTraits, Instance, List

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.verifier import VerifierError
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.notification_listeners.base_notification_listener_model \
    import BaseNotificationListenerModel


log = logging.getLogger(__name__)


class Workflow(HasStrictTraits):
    """Model object that represents the Workflow as a whole"""
    #: Contains the factory-specific MCO Model object.
    #: Can be None if no MCO has been specified yet.
    mco = Instance(BaseMCOModel, allow_none=True)

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
        available_data_values = self.mco.bind_parameters(data_values)

        for index, layer in enumerate(self.execution_layers):
            log.info("Computing data layer {}".format(index))
            ds_results = layer.execute_layer(available_data_values)
            available_data_values += ds_results

        log.info("Aggregating KPI data")

        kpi_results = self.mco.bind_kpis(data_values)

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

        if not self.mco:
            errors.append(
                VerifierError(
                    subject=self,
                    global_error="Workflow has no MCO",
                )
            )
        else:
            errors += self.mco.verify()

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
