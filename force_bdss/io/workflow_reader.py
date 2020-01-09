from functools import wraps
import json
import logging

from traits.api import HasStrictTraits, Instance

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.i_factory_registry import IFactoryRegistry
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.core.workflow import Workflow, WorkflowAttributeWarning

logger = logging.getLogger(__name__)

SUPPORTED_FILE_VERSIONS = ["1"]


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

    def read(self, file):
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
        json_data = json.load(file)

        try:
            version = json_data["version"]
        except KeyError:
            logger.error("File missing version information")
            raise InvalidFileException(
                "Corrupted input file, no version specified"
            )

        if version not in SUPPORTED_FILE_VERSIONS:
            logger.error(
                "File contains version {} that is not in the "
                "list of supported versions {}".format(
                    version, SUPPORTED_FILE_VERSIONS
                )
            )
            raise InvalidVersionException(
                "File version {} not supported".format(json_data["version"])
            )

        try:
            wf_data = json_data["workflow"]
            wf = self.read_dict(wf_data)
        except KeyError as e:
            msg = (
                "Could not read file {}. Unable to find key {}. "
                "The file might be corrupted or unsupported.".format(file, e)
            )
            logger.exception(msg)
            raise InvalidFileException(msg)

        return wf

    def read_dict(self, wf_data):
        """Read a dictionary containing workflow data and return a Workflow
        object

        Parameters
        ----------
        wf_data: Data
            The dictionary containing the workflow data.
        """
        wf = Workflow()

        wf.mco_model = self._extract_mco(wf_data)
        wf.execution_layers[:] = self._extract_execution_layers(wf_data)
        wf.notification_listeners[:] = self._extract_notification_listeners(
            wf_data
        )
        return wf

    @deprecated_wf_format
    def _extract_mco(self, wf_data):
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
                "Could not read file. "
                "The plugin responsible for the missing "
                "key '{}' may be missing or broken.".format(mco_id)
            )
        model_data = wf_data["mco_model"]["model_data"]
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
                "Unable to create model for MCO {}: {}. "
                "This is likely due to a coding error in the plugin. "
                "Check the logs for more information.".format(mco_id, e)
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
        for el_entry in wf_data["execution_layers"]:
            layer = ExecutionLayer()

            for ds_entry in el_entry:
                ds_id = ds_entry["id"]

                try:
                    ds_factory = registry.data_source_factory_by_id(ds_id)
                except KeyError:
                    raise MissingPluginException(
                        "Could not read file. "
                        "The plugin responsible for the missing data source "
                        "key '{}' may be missing or broken.".format(ds_id)
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
                        "Unable to create model for DataSource {} : {}. "
                        "This is likely due to a coding "
                        "error in the plugin. Check the logs for more "
                        "information.".format(ds_id, e)
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
                    "Could not read file. "
                    "The plugin responsible for the missing MCO '{}' "
                    "parameter key '{}' may be missing or broken.".format(
                        mco_id, parameter_id
                    )
                )

            try:
                model = factory.create_model(p["model_data"])
            except Exception as e:
                msg = (
                    "Unable to create model for MCO {} parameter {} : {}. "
                    "This is likely due to an error in the plugin. "
                    "Check the logs for more information.".format(
                        mco_id, parameter_id, e
                    )
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
        for nl_entry in wf_data["notification_listeners"]:
            nl_id = nl_entry["id"]
            try:
                nl_factory = registry.notification_listener_factory_by_id(
                    nl_id
                )
            except KeyError:
                raise MissingPluginException(
                    "Could not read file. "
                    "The plugin responsible for the missing "
                    "notification listener key '{}' may be missing "
                    "or broken.".format(nl_id)
                )

            model_data = nl_entry["model_data"]

            try:
                model = nl_factory.create_model(model_data)
            except Exception as e:
                msg = (
                    "Unable to create model for Notification Listener "
                    "{} : {}. This is likely due to an error in the plugin. "
                    "Check the logs for more information.".format(nl_id, e)
                )
                logger.exception(msg)
                raise ModelInstantiationFailedException(msg)

            listeners.append(model)

        return listeners
