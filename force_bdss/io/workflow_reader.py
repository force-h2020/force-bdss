import json
import logging

from traits.api import HasStrictTraits, Instance, Str

from force_bdss.core.i_factory_registry import IFactoryRegistry
from force_bdss.core.workflow import Workflow

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


class WorkflowReader(HasStrictTraits):
    """
    Reads the workflow from a file.
    """

    #: The Factory registry. The reader needs it to create the
    #: specific model objects.
    factory_registry = Instance(IFactoryRegistry)

    #: The version of the workflow data file format
    workflow_format_version = Str()

    def __init__(self, factory_registry, *args, **kwargs):
        """Initializes the reader.

        Parameters
        ----------
        factory_registry: FactoryRegistryPlugin
            The factory registry that provides lookup services
            for a factory identified by a given id.
        """
        super().__init__(factory_registry=factory_registry, *args, **kwargs)

    def read(self, path):
        """Reads the file and returns a Workflow object.
        If any problem is found, raises an InvalidFileException or a
        derived, more specialized exception.

        Parameters
        ----------
        path: str
            A path to file containing the serialized data of the workflow.

        Returns
        -------
        Workflow
            An instance of the model tree, rooted at Workflow.
        """
        json_data = self.load_data(path)

        self.workflow_format_version = self._extract_version(json_data)

        workflow_data = self._preprocess_workflow_data(json_data)

        workflow = Workflow.from_json(self.factory_registry, workflow_data)
        return workflow

    def load_data(self, filepath):
        """ Loads the data from file located at `filepath` in json
        format.

        Parameters
        ----------
        filepath: str
            path to file to load

        Returns
        ----------
        json_data: dict
            data parsed from json-formatted file
        """
        with open(filepath, "r") as input_file:
            json_data = json.load(input_file)
        return json_data

    def _extract_version(self, json_data):
        """ Verifies the workflow.json version. Checks if it is
        supported by the current version of BDSS.

        Parameters
        ----------
        json_data: dict
            Dictionary with complete serialized form of a workflow
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

    def _preprocess_workflow_data(self, json_data):
        workflow_data = json_data.get("workflow", {})
        workflow_data["mco_model"] = workflow_data.get("mco_model", None)
        workflow_data["execution_layers"] = workflow_data.get(
            "execution_layers", []
        )
        for i, layer in enumerate(workflow_data["execution_layers"]):
            if self.workflow_format_version == "1":
                workflow_data["execution_layers"][i] = {"data_sources": layer}

        workflow_data["notification_listeners"] = workflow_data.get(
            "notification_listeners", []
        )

        return workflow_data
