from copy import deepcopy
import logging

from traits.api import (
    HasStrictTraits,
    Instance,
    List,
    provides,
    on_trait_change,
    Bool,
)

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.verifier import VerifierError
from force_bdss.events.event_notifier_mixin import EventNotifierMixin
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.notification_listeners.base_notification_listener_model \
    import BaseNotificationListenerModel
from force_bdss.mco.i_evaluator import IEvaluator
from force_bdss.core.data_value import DataValue
from force_bdss.utilities import pop_dunder_recursive, nested_getstate
from force_bdss.events.mco_events import MCOTerminateEvent


log = logging.getLogger(__name__)


@provides(IEvaluator)
class Workflow(EventNotifierMixin, HasStrictTraits):
    """Model object that represents the Workflow as a whole"""

    #: The Workflow BaseMCOModel object.
    #: Can be None if no BaseMCOModel has been specified yet.
    mco_model = Instance(BaseMCOModel, allow_none=True)

    #: The execution layers. Execution starts from the first layer,
    #: where all data sources are executed in sequence. It then passes all
    #: the computed data to the second layer, then the third etc.
    execution_layers = List(ExecutionLayer)

    #: Contains information about the listeners to be setup
    notification_listeners = List(BaseNotificationListenerModel)

    _terminate = Bool(False, visible=False, transient=True)

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
        Generates the `mco_model`, list of `execution_layers`, list of
        `notification_listeners`, and then creates a `Workflow` instance with
        these objects.

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
        workflow_data = deepcopy(json_data)

        workflow_data["mco_model"] = cls._extract_mco_model(
            factory_registry, workflow_data
        )

        workflow_data["execution_layers"] = cls._extract_execution_layers(
            factory_registry, workflow_data
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
        mco_data = workflow_data["mco_model"]
        if mco_data is None:
            return None
        mco_factory = factory_registry.mco_factory_by_id(mco_data["id"])
        return mco_factory.model_class.from_json(
            mco_factory, mco_data["model_data"]
        )

    @staticmethod
    def _extract_execution_layers(factory_registry, workflow_data):
        """ Generates the List(ExecutionLayer) from the `workflow_data` dictionary.

        Parameters
        ----------
        factory_registry: IFactoryRegistry
            Generating factory registry for the data sources inside the
            execution layers
        workflow_data: dict
            Dictionary with the content of the `ExecutionLayer`s in
            serialized format

        Returns
        -------
        execution_layers: List(ExecutionLayer)
            list of ExecutionLayer instances.
        """
        execution_layers = []
        for layer_data in workflow_data["execution_layers"]:
            layer = ExecutionLayer.from_json(factory_registry, layer_data)
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

    @on_trait_change("mco_model:event,execution_layers:event")
    def notify_driver_event(self, event):
        """ Captures a BaseDriverEvent and passes it on to OptimizeOperation

        Parameters
        ----------
        event: BaseDriverEvent
            The BaseDriverEvent that has been changed
        """
        self.notify(event)

        self._scan_pending_terminate_events()

    def _scan_pending_terminate_events(self):
        """ Iterates over the `pending_event` attribute of the notification
        listeners and checks whether any `MCOTerminateEvent` are pending.
        If there is such event pending, sets the `_terminate` attribute to True.
        """
        for notification_listener in self.notification_listeners:
            try:
                pending_event = notification_listener.get_pending_event()
            except AttributeError:
                pass
            else:
                if isinstance(pending_event, MCOTerminateEvent):
                    self._terminate = True
                    notification_listener.resolve_pending_event()

    def terminating(self):
        return self._terminate
