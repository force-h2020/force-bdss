import json
import logging

from traits.api import HasStrictTraits, Instance

from ..bundle_registry_plugin import BundleRegistryPlugin
from ..workspecs.workflow import Workflow

SUPPORTED_FILE_VERSIONS = ["1"]


class InvalidFileException(Exception):
    """Raised if the file is invalid for some reason"""


class InvalidVersionException(InvalidFileException):
    """Raised if the version tag does not satisfy the currently
    supported list."""


class WorkflowReader(HasStrictTraits):
    """
    Reads the workflow from a file.
    """
    #: The bundle registry. The reader needs it to create the
    #: bundle-specific model objects.
    bundle_registry = Instance(BundleRegistryPlugin)

    def __init__(self,
                 bundle_registry,
                 *args,
                 **kwargs):
        """Initializes the reader.

        Parameters
        ----------
        bundle_registry: BundleRegistryPlugin
            The bundle registry that provides lookup services
            for a bundle identified by a given id.
        """
        self.bundle_registry = bundle_registry

        super(WorkflowReader, self).__init__(*args, **kwargs)

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
        """
        json_data = json.load(file)

        try:
            version = json_data["version"]
        except KeyError:
            logging.error("File missing version information")
            raise InvalidFileException("Corrupted input file, no version"
                                       " specified")

        if version not in SUPPORTED_FILE_VERSIONS:
            logging.error(
                "File contains version {} that is not in the "
                "list of supported versions {}".format(
                    version, SUPPORTED_FILE_VERSIONS)
            )
            raise InvalidVersionException(
                "File version {} not supported".format(json_data["version"]))

        wf = Workflow()

        try:
            wf_data = json_data["workflow"]
            wf.mco = self._extract_mco(wf_data)
            wf.data_sources[:] = self._extract_data_sources(wf_data)
            wf.kpi_calculators[:] = self._extract_kpi_calculators(wf_data)
        except KeyError as e:
            logging.exception("Could not read file")
            raise InvalidFileException("Could not read file. "
                                       "Unable to find key {}".format(e))
        return wf

    def _extract_mco(self, wf_data):
        """Extracts the MCO from the workflow dictionary data.

        Parameters
        ----------
        wf_data: dict
            the content of the workflow key in the top level dictionary data.

        Returns
        -------
        a BaseMCOModel instance of the bundle-specific MCO driver, or None
        if no MCO is specified in the file (as in the case of premature
        saving).
        """
        registry = self.bundle_registry

        mco_data = wf_data.get("mco")
        if mco_data is None:
            # The file was saved without setting an MCO.
            # The file is valid, we simply can't run any optimization yet.
            return None

        mco_id = mco_data["id"]
        mco_bundle = registry.mco_bundle_by_id(mco_id)
        model_data = wf_data["mco"]["model_data"]
        model_data["parameters"] = self._extract_mco_parameters(
            mco_id,
            model_data["parameters"])
        model = mco_bundle.create_model(
            wf_data["mco"]["model_data"])
        return model

    def _extract_data_sources(self, wf_data):
        """Extracts the data sources from the workflow dictionary data.

        Parameters
        ----------
        wf_data: dict
            the content of the workflow key in the top level dictionary data.

        Returns
        -------
        list of BaseDataSourceModel instances. Each BaseDataSourceModel is an
        instance of the bundle specific model class. The list can be empty.
        """
        registry = self.bundle_registry

        data_sources = []
        for ds_entry in wf_data["data_sources"]:
            ds_id = ds_entry["id"]
            ds_bundle = registry.data_source_bundle_by_id(ds_id)
            data_sources.append(ds_bundle.create_model(ds_entry["model_data"]))

        return data_sources

    def _extract_kpi_calculators(self, wf_data):
        """Extracts the KPI calculators from the workflow dictionary data.

        Parameters
        ----------
        wf_data: dict
            the content of the workflow key in the top level dictionary data.

        Returns
        -------
        list of BaseKPICalculatorModel instances. Each BaseKPICalculatorModel
        is an instance of the bundle specific model class. The list can be
        empty.
        """
        registry = self.bundle_registry

        kpi_calculators = []
        for kpic_entry in wf_data["kpi_calculators"]:
            kpic_id = kpic_entry["id"]
            kpic_bundle = registry.kpi_calculator_bundle_by_id(kpic_id)

            kpi_calculators.append(
                kpic_bundle.create_model(kpic_entry["model_data"]))

        return kpi_calculators

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
        registry = self.bundle_registry

        parameters = []

        for p in parameters_data:
            id = p["id"]
            factory = registry.mco_parameter_factory_by_id(mco_id, id)
            model = factory.create_model(p["model_data"])
            parameters.append(model)

        return parameters
