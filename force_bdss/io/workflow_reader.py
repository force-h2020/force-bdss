import json

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
        registry = self.bundle_registry

        try:
            version = json_data["version"]
        except KeyError:
            raise InvalidFileException("Corrupted input file, no version"
                                       " specified")

        if version not in SUPPORTED_FILE_VERSIONS:
            raise InvalidVersionException(
                "File version {} not supported".format(json_data["version"]))

        wf = Workflow()

        mco_id = json_data["multi_criteria_optimizer"]["id"]
        mco_bundle = registry.mco_bundle_by_id(mco_id)
        wf.multi_criteria_optimizer = mco_bundle.create_model(
            json_data["multi_criteria_optimizer"]["model_data"])

        for ds_entry in json_data["data_sources"]:
            ds_id = ds_entry["id"]
            ds_bundle = registry.data_source_bundle_by_id(ds_id)
            wf.data_sources.append(ds_bundle.create_model(
                ds_entry["model_data"]))

        for kpic_entry in json_data["kpi_calculators"]:
            kpic_id = kpic_entry["id"]
            kpic_bundle = registry.kpi_calculator_bundle_by_id(kpic_id)
            wf.kpi_calculators.append(kpic_bundle.create_model(
                kpic_entry["model_data"]))

        return wf
