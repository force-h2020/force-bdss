import json
import logging

from traits.api import HasStrictTraits, Instance

from ..workspecs.workflow import Workflow
from ..bundle_registry_plugin import BundleRegistryPlugin

SUPPORTED_FILE_VERSIONS = ["1"]


class InvalidFileException(Exception):
    pass


class InvalidVersionException(InvalidFileException):
    pass


class WorkflowReader(HasStrictTraits):
    bundle_registry = Instance(BundleRegistryPlugin)

    def __init__(self, bundle_registry, *args, **kwargs):
        self.bundle_registry = bundle_registry

        super(WorkflowReader, self).__init__(*args, **kwargs)

    def read(self, file):
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
            wf.multi_criteria_optimizer = self._extract_mco(wf_data)
            wf.data_sources[:] = self._extract_data_sources(wf_data)
            wf.kpi_calculators[:] = self._extract_kpi_calculators(wf_data)
        except KeyError as e:
            logging.exception("Could not read file")
            raise InvalidFileException("Could not read file. "
                                       "Unable to find key {}".format(e))
        return wf

    def _extract_mco(self, json_data):
        registry = self.bundle_registry

        mco_id = json_data["multi_criteria_optimizer"]["id"]
        mco_bundle = registry.mco_bundle_by_id(mco_id)
        return mco_bundle.create_model(
            json_data["multi_criteria_optimizer"]["model_data"])

    def _extract_data_sources(self, json_data):
        registry = self.bundle_registry

        data_sources = []
        for ds_entry in json_data["data_sources"]:
            ds_id = ds_entry["id"]
            ds_bundle = registry.data_source_bundle_by_id(ds_id)
            data_sources.append(ds_bundle.create_model(ds_entry["model_data"]))

        return data_sources

    def _extract_kpi_calculators(self, json_data):
        registry = self.bundle_registry

        kpi_calculators = []
        for kpic_entry in json_data["kpi_calculators"]:
            kpic_id = kpic_entry["id"]
            kpic_bundle = registry.kpi_calculator_bundle_by_id(kpic_id)

            kpi_calculators.append(
                kpic_bundle.create_model(kpic_entry["model_data"]))

        return kpi_calculators
