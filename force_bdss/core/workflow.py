from copy import deepcopy
import logging

from traits.api import HasStrictTraits, Instance, List

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.verifier import VerifierError
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.notification_listeners.base_notification_listener_model \
    import BaseNotificationListenerModel
from force_bdss.io.workflow_writer import pop_dunder_recursive, nested_getstate

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

    def __getstate__(self):
        """ Returns state dictionary of the object. For a nested dict,
        __getstate__ is applied to zero level items and first level items.
        """
        state = pop_dunder_recursive(super().__getstate__())
        state = nested_getstate(state)
        return state

    @classmethod
    def from_json(cls, factory_registry, json_data):
        """ Generates the `Workflow` instance from the `json_data` dictionary.
        Explicitly populates the workflow attributes with instances from the
        `factory_registry` and data from `json_data`.

        Parameters
        ----------
        factory_registry: IFactoryRegistry
            Generating factory registry for the MCOModel of the workflow
        json_data: dict
            Dictionary with the content of the `Workflow`'s in serialized
            format

        Returns
        -------
        workflow: Workflow
            `Workflow` instance corresponding to the `json_data`
        """
        workflow_data = deepcopy(json_data["workflow"])

        workflow_data["mco_model"] = cls._extract_mco_model(
            factory_registry, workflow_data
        )

        workflow_data["execution_layers"] = cls._extract_execution_layers(
            factory_registry, workflow_data, json_data["version"]
        )

        workflow_data[
            "notification_listeners"
        ] = cls._extract_notification_listeners(
            factory_registry, workflow_data
        )

        workflow = cls(**workflow_data)
        return workflow

    @staticmethod
    def _extract_mco_model(factory_registry, workflow_data):
        """ Generates the BaseMCOModel from the `workflow_data` dictionary.

        Parameters
        ----------
        factory_registry: IFactoryRegistry
            Generating factory registry for the MCOModel of the
            workflow
        workflow_data: dict
            Dictionary with the content of the `BaseMCOModel`s in
            serialized format

        Returns
        -------
        mco_model: BaseMCOModel
            `BaseMCOModel` instance
        """
        mco_data = workflow_data.get("mco_model")
        if mco_data is None:
            return None
        mco_factory = factory_registry.mco_factory_by_id(mco_data["id"])
        return mco_factory.model_class.from_json(
            mco_factory, mco_data["model_data"]
        )

    @staticmethod
    def _extract_execution_layers(factory_registry, workflow_data, version):
        """ Generates the List(ExecutionLayer) from the `workflow_data` dictionary.

        Parameters
        ----------
        factory_registry: IFactoryRegistry
            Generating factory registry for the data sources inside the
            execution layers
        workflow_data: dict
            Dictionary with the content of the `ExecutionLayer`s in
            serialized format
        version: str
            Workflow file format. Indicates the structure of the
            `workflow_data`

        Returns
        -------
        execution_layers: List(ExecutionLayer)
            list of ExecutionLayer instances.
        """
        execution_layers = []
        for layer_data in workflow_data["execution_layers"]:

            if version == "1":
                data = {"data_sources": layer_data}
            else:
                data = layer_data

            layer = ExecutionLayer.from_json(factory_registry, data)
            execution_layers.append(layer)

        return execution_layers

    @staticmethod
    def _extract_notification_listeners(factory_registry, workflow_data):
        """ Generates the List(BaseNotificationListenerModel) from the
        `workflow_data` dictionary.

        Parameters
        ----------
        factory_registry: IFactoryRegistry
            Generating factory registry for the notification listeners of the
            workflow
        workflow_data: dict
            Dictionary with the content of the `NotificationListener`s in
            serialized format

        Returns
        -------
        listeners: List(BaseNotificationListenerModel)
            list of BaseNotificationListenerModel instances.
        """
        listeners = []
        for listener_data in workflow_data["notification_listeners"]:
            lis_factory = factory_registry.notification_listener_factory_by_id(
                listener_data["id"]
            )
            listener = lis_factory.create_model(listener_data["model_data"])
            listeners.append(listener)
        return listeners
