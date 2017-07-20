import json
from traits.api import Instance, HasStrictTraits

from ..bundle_registry_plugin import BundleRegistryPlugin


class WorkflowWriter(HasStrictTraits):
    def write(self, workflow, f):
        data = {
            "version": "1",
            "workflow": {}
        }

        wf_data = data["workflow"]
        wf_data["multi_criteria_optimizer"] = {
            "id": workflow.multi_criteria_optimizer.bundle.id,
            "model_data": workflow.multi_criteria_optimizer.__getstate__()
        }
        kpic_data = []
        for kpic in workflow.kpi_calculators:
            kpic_data.append({
                "id": kpic.bundle.id,
                "model_data": kpic.__getstate__()}
            )

        wf_data["kpi_calculators"] = kpic_data

        ds_data = []
        for ds in workflow.data_sources:
            ds_data.append({
                "id": ds.bundle.id,
                "model_data": ds.__getstate__()
            })

        wf_data["data_sources"] = ds_data

        json.dump(data, f)
