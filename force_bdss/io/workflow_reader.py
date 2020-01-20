from copy import deepcopy
from functools import wraps
import json
import logging

from traits.api import HasStrictTraits, Instance, Str

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.i_factory_registry import IFactoryRegistry
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.core.workflow import Workflow, WorkflowAttributeWarning

logger = logging.getLogger(__name__)

SUPPORTED_FILE_VERSIONS = ["1", "1.1"]


class BaseWorkflowReaderException(Exception):
    """Base exception for the reader errors."""


class InvalidFileException(BaseWorkflowReaderException):
    """Raised for a generic file being invalid for some
    reason, e.g. incorrect format or missing keys.
    """


class InvalidVersionException(BaseWorkflowReaderException):
    """Raised if the version tag does not satisfy the currently
    supported list."""


class MissingPluginException(BaseWorkflowReaderException):
    """Raised if the file requires a plugin we cannot find."""


class ModelInstantiationFailedException(BaseWorkflowReaderException):
    """Raised if we can't instantiate the model from a plugin"""


def deprecated_wf_format(mco_reader):
    @wraps(mco_reader)
    def inner(self, wf_data):
        if "mco" in wf_data and "mco_model" not in wf_data:
            wf_data["mco_model"] = wf_data.pop("mco")
            WorkflowAttributeWarning.warn()
        return mco_reader(self, wf_data)

    return inner


class WorkflowReader(HasStrictTraits):
    """
    Reads the workflow from a file.
    """

    #: The Factory registry. The reader needs it to create the
    #: specific model objects.
    factory_registry = Instance(IFactoryRegistry)

    workflow_format_version = Str()

    def __init__(self, factory_registry, *args, **kwargs):
        """Initializes the reader.

        Parameters
        ----------
        factory_registry: FactoryRegistryPlugin
            The factory registry that provides lookup services
            for a factory identified by a given id.
        """
        super(WorkflowReader, self).__init__(
            factory_registry=factory_registry, *args, **kwargs
        )

    def read(self, path):
        """Reads the file and returns a Workflow object.
        If any problem is found, raises an InvalidFileException or a
        derived, more specialized exception.

        Parameters
        ----------
        file: File
            A file object containing the data of the workflow in the
            appropriate json format.

        Returns
        -------
        Workflow
            An instance of the model tree, rooted at Workflow.

        Raises
        ------
        InvalidFileException
            Raised if the file is corrupted or cannot be read by this reader.

        InvalidVersionException
            Raised if the version is not supported.

        MissingPluginException
            The file cannot be opened because it needs a plugin that is not
            available.

        ModelInstantiationFailedException
            When instantiating the model for a given plugin, an exception
            occurred. This is likely due to a coding error in the plugin.

        """
        json_data = self.load_data(path)

        self.workflow_format_version = self._extract_version(json_data)
        workflow = Workflow.from_json(self.factory_registry, json_data)
        return workflow

    def load_data(self, filepath):
        """ Loads the data from file located at `filepath` in json
        format.

        Parameters
        ----------
        filepath: str
            path to file to load in string format

        Returns
        ----------
        json_data: dict
            data parsed from json-formatted file
        """
        with open(filepath, "r") as input_file:
            json_data = json.load(input_file)
        return json_data

    def _extract_workflow(self, json_data):
        try:
            wf_data = json_data["workflow"]
            wf = Workflow()

            wf.mco_model = self._extract_mco_model(wf_data)
            wf.execution_layers[:] = self._extract_execution_layers(wf_data)

            listeners = self._extract_notification_listeners(wf_data)
            wf.notification_listeners[:] = listeners
        except KeyError as e:
            msg = (
                f"Invalid input file format: unable to find key {e}."
                "The file might be corrupted or unsupported."
            )
            logger.exception(msg)
            raise InvalidFileException(msg)

        return wf

    def _extract_version(self, json_data):
        """ Verifies the workflow.json version. Checks if it is
        supported by the current version of BDSS.
        """
        error_prefix = "Invalid input file format: "
        try:
            version = json_data["version"]
        except KeyError:
            version_error_message = error_prefix + "no version specified"
            logger.error(version_error_message)
            raise InvalidFileException(version_error_message)

        if version not in SUPPORTED_FILE_VERSIONS:
            error_postfix = (
                f" version {version} is not in the "
                f"list of supported versions {SUPPORTED_FILE_VERSIONS}"
            )
            version_error_message = error_prefix + error_postfix
            logger.error(version_error_message)
            raise InvalidVersionException(version_error_message)

        return version

    @deprecated_wf_format
    def _extract_mco_model(self, wf_data):
        """Extracts the MCO from the workflow dictionary data.

        Parameters
        ----------
        wf_data: dict
            the content of the workflow key in the top level dictionary data.

        Returns
        -------
        a BaseMCOModel instance of the specific MCO driver, or None
        if no MCO is specified in the file (as in the case of premature
        saving).
        """
        registry = self.factory_registry

        mco_data = wf_data.get("mco_model")
        if mco_data is None:
            # The file was saved without setting an MCO.
            # The file is valid, we simply can't run any optimization yet.
            return None

        mco_id = mco_data["id"]
        try:
            mco_factory = registry.mco_factory_by_id(mco_id)
        except KeyError:
            raise MissingPluginException(
                "Invalid input file format: "
                f"the plugin responsible for the key '{mco_id}'"
                " may be missing or broken."
            )
        # `deepcopy` is required because we deserialize the mco_parameters
        # and kpis inplace.
        model_data = deepcopy(wf_data["mco_model"]["model_data"])
        model_data["parameters"] = self._extract_mco_parameters(
            mco_id, model_data["parameters"]
        )
        model_data["kpis"] = self._extract_kpi_specifications(
            model_data["kpis"]
        )

        try:
            model = mco_factory.create_model(model_data)
        except Exception as e:
            msg = (
                f"Unable to create model for MCO {mco_id}: {e}. "
                "This is likely due to a coding error in the plugin. "
                "Check the logs for more information."
            )

            logger.exception(msg)
            raise ModelInstantiationFailedException(msg)
        return model

    def _extract_execution_layers(self, wf_data):
        """Extracts the data sources from the workflow dictionary data.

        Parameters
        ----------
        wf_data: dict
            the content of the workflow key in the top level dictionary data.

        Returns
        -------
        list of BaseDataSourceModel instances. Each BaseDataSourceModel is an
        instance of the specific model class. The list can be empty.
        """
        registry = self.factory_registry

        layers = []
        for el_entry in deepcopy(wf_data["execution_layers"]):
            layer = ExecutionLayer()

            if self.workflow_format_version == "1":
                ds_iterable = el_entry
            elif self.workflow_format_version == "1.1":
                ds_iterable = el_entry["data_sources"]

            for ds_entry in ds_iterable:
                ds_id = ds_entry["id"]

                try:
                    ds_factory = registry.data_source_factory_by_id(ds_id)
                except KeyError:
                    raise MissingPluginException(
                        "Invalid input file format: "
                        "the plugin responsible for the data source "
                        f"key '{ds_id}' may be missing or broken."
                    )

                model_data = ds_entry["model_data"]
                model_data["input_slot_info"] = self._extract_input_slot_info(
                    model_data["input_slot_info"]
                )
                model_data[
                    "output_slot_info"
                ] = self._extract_output_slot_info(
                    model_data["output_slot_info"]
                )

                try:
                    ds_model = ds_factory.create_model(model_data)
                except Exception as e:
                    msg = (
                        f"Unable to create model for DataSource {ds_id}: {e}. "
                        "This is likely due to a coding "
                        "error in the plugin. Check the logs for more "
                        "information."
                    )
                    logger.exception(msg)
                    raise ModelInstantiationFailedException(msg)

                layer.data_sources.append(ds_model)

            layers.append(layer)

        return layers

    def _extract_mco_parameters(self, mco_id, parameters_data):
        """Extracts the MCO parameters from the data as dictionary.

        Parameters
        ----------
        parameters_data: dict
            The content of the parameter data key in the MCO model data.

        Returns
        -------
        List of instances of a subclass of BaseMCOParameter
        """
        registry = self.factory_registry

        parameters = []

        for p in parameters_data:
            parameter_id = p["id"]
            try:
                factory = registry.mco_parameter_factory_by_id(
                    mco_id, parameter_id
                )
            except KeyError:
                raise MissingPluginException(
                    "Invalid input file format:  "
                    f"the plugin responsible for the MCO '{mco_id}' "
                    f"parameter key '{parameter_id}' may be missing or broken."
                )

            try:
                model = factory.create_model(p["model_data"])
            except Exception as e:
                msg = (
                    f"Unable to create model for MCO {mco_id} parameter "
                    f"{parameter_id}: {e} "
                    "This is likely due to an error in the plugin. "
                    "Check the logs for more information."
                )
                logger.exception(msg)
                raise ModelInstantiationFailedException(msg)

            parameters.append(model)

        return parameters

    def _extract_kpi_specifications(self, info):
        return [KPISpecification(**d) for d in info]

    def _extract_input_slot_info(self, info):
        return [InputSlotInfo(**d) for d in info]

    def _extract_output_slot_info(self, info):
        return [OutputSlotInfo(**d) for d in info]

    def _extract_notification_listeners(self, wf_data):
        registry = self.factory_registry
        listeners = []
        for nl_entry in deepcopy(wf_data["notification_listeners"]):
            nl_id = nl_entry["id"]
            try:
                nl_factory = registry.notification_listener_factory_by_id(
                    nl_id
                )
            except KeyError:
                raise MissingPluginException(
                    "Invalid input file format: "
                    "the plugin responsible for the "
                    f"notification listener key '{nl_id}' may be missing "
                    "or broken."
                )

            model_data = nl_entry["model_data"]

            try:
                model = nl_factory.create_model(model_data)
            except Exception as e:
                msg = (
                    "Unable to create model for Notification Listener "
                    f"{nl_id}: {e}. "
                    "This is likely due to an error in the plugin. "
                    "Check the logs for more information."
                )
                logger.exception(msg)
                raise ModelInstantiationFailedException(msg)

            listeners.append(model)

        return listeners
