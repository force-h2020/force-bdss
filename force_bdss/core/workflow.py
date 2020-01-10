import logging

from traits.api import HasStrictTraits, Instance, List, Property

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.verifier import VerifierError
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.notification_listeners.base_notification_listener_model \
    import BaseNotificationListenerModel


log = logging.getLogger(__name__)


class WorkflowAttributeWarning:
    warning_message = (
        "The Workflow object format with 'mco' attribute is now"
        " deprecated. Please use 'mco_model' attribute instead."
    )

    @classmethod
    def warn(cls):
        log.warning(cls.warning_message)


class Workflow(HasStrictTraits):
    """Model object that represents the Workflow as a whole"""

    #: The Workflow provate MCOModel object.
    #: Can be None if no MCOModel has been specified yet.
    _mco_model = Instance(BaseMCOModel, allow_none=True)

    #: The Workflow public MCOModel property.
    #: Implement getter and setter methods for data verification.
    mco_model = Property(depends_on="_mco_model")

    #: The execution layers. Execution starts from the first layer,
    #: where all data sources are executed in sequence. It then passes all
    #: the computed data to the second layer, then the third etc.
    execution_layers = List(ExecutionLayer)

    #: Contains information about the listeners to be setup
    notification_listeners = List(BaseNotificationListenerModel)

    def _get_mco_model(self):
        """ This is a public method to get the Workflow MCOModel attribute.
        Direct access to `self._mco_model` for assignment is unsafe.
        This method is safe and includes necessary verification steps prior
        to assigning the `mco_model` to `self._mco_model`.
        """
        return self._mco_model

    def _set_mco_model(self, mco_model):
        """ This is a public method to set the Workflow MCOModel attribute.
        Direct access to `self._mco_model` for assignment is unsafe.
        This method is safe and includes necessary verification steps prior
        to assigning the `mco_model` to `self._mco_model`.
        """
        self._mco_model = mco_model

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
