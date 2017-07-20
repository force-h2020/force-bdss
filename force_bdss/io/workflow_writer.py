import json
from traits.api import HasStrictTraits


class WorkflowWriter(HasStrictTraits):
    """A Writer for writing the Workflow onto disk.
    """
    def write(self, workflow, f):
        """Writes the workflow model object to a file f in JSON format.

        Parameters
        ----------
        workflow: Workflow
            The Workflow instance to write to file

        f: File
            A file object on which to write the workflow, properly serialized
            into JSON.
        """
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