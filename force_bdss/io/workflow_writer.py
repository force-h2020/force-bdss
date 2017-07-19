import json
from traits.api import Instance, HasStrictTraits

from ..bundle_registry_plugin import BundleRegistryPlugin


class WorkflowWriter(HasStrictTraits):
    bundle_registry = Instance(BundleRegistryPlugin)

    def __init__(self, bundle_registry, *args, **kwargs):
        self.bundle_registry = bundle_registry

        super(WorkflowWriter, self).__init__(*args, **kwargs)

    def write(self, workflow, f):
        data = {
            "version": "1",
        }

        data["multi_criteria_optimizer"] = \
            workflow.multi_criteria_optimizer.__getstate__()

        kpic_data = []
        for kpic in workflow.kpi_calculators:
            kpic_data.append(kpic.__getstate__())

        data["kpi_calculators"] = kpic_data

        ds_data = []
        for ds in workflow.data_sources:
            ds_data.append(ds.__getstate__())

        data["data_sources"] = ds_data

        json.dump(data, f)
