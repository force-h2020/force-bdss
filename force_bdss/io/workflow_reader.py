import json
import logging

from traits.api import HasStrictTraits, Instance

from force_bdss.core.input_slot_map import InputSlotMap
from force_bdss.core.workflow import Workflow
from ..factory_registry_plugin import IFactoryRegistryPlugin

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
    #: The Factory registry. The reader needs it to create the
    #: specific model objects.
    factory_registry = Instance(IFactoryRegistryPlugin)

    def __init__(self,
                 factory_registry,
                 *args,
                 **kwargs):
        """Initializes the reader.

        Parameters
        ----------
        factory_registry: FactoryRegistryPlugin
            The factory registry that provides lookup services
            for a factory identified by a given id.
        """
        self.factory_registry = factory_registry

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
            wf.notification_listeners[:] = \
                self._extract_notification_listeners(wf_data)
        except KeyError as e:
            logging.exception("Could not read file {}".format(file))
            raise InvalidFileException("Could not read file {}. "
                                       "Unable to find key {}".format(file, e))
        return wf

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

        mco_data = wf_data.get("mco")
        if mco_data is None:
            # The file was saved without setting an MCO.
            # The file is valid, we simply can't run any optimization yet.
            return None

        mco_id = mco_data["id"]
        mco_factory = registry.mco_factory_by_id(mco_id)
        model_data = wf_data["mco"]["model_data"]
        model_data["parameters"] = self._extract_mco_parameters(
            mco_id,
            model_data["parameters"])
        model = mco_factory.create_model(
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
        instance of the specific model class. The list can be empty.
        """
        registry = self.factory_registry

        data_sources = []
        for ds_entry in wf_data["data_sources"]:
            ds_id = ds_entry["id"]
            ds_factory = registry.data_source_factory_by_id(ds_id)
            model_data = ds_entry["model_data"]
            model_data["input_slot_maps"] = self._extract_input_slot_maps(
                model_data["input_slot_maps"]
            )
            data_sources.append(ds_factory.create_model(model_data))

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
        is an instance of the specific model class. The list can be
        empty.
        """
        registry = self.factory_registry

        kpi_calculators = []
        for kpic_entry in wf_data["kpi_calculators"]:
            kpic_id = kpic_entry["id"]
            kpic_factory = registry.kpi_calculator_factory_by_id(kpic_id)
            model_data = kpic_entry["model_data"]
            model_data["input_slot_maps"] = self._extract_input_slot_maps(
                model_data["input_slot_maps"]
            )

            kpi_calculators.append(
                kpic_factory.create_model(model_data)
            )

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
        registry = self.factory_registry

        parameters = []

        for p in parameters_data:
            id = p["id"]
            factory = registry.mco_parameter_factory_by_id(mco_id, id)
            model = factory.create_model(p["model_data"])
            parameters.append(model)

        return parameters

    def _extract_input_slot_maps(self, maps_data):
        return [InputSlotMap(**d) for d in maps_data]

    def _extract_notification_listeners(self, wf_data):
        registry = self.factory_registry
        listeners = []
        for nl_entry in wf_data["notification_listeners"]:
            nl_id = nl_entry["id"]
            nl_factory = registry.notification_listener_factory_by_id(nl_id)
            model_data = nl_entry["model_data"]
            listeners.append(nl_factory.create_model(model_data))

        return listeners
