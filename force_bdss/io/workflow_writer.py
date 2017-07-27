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
        wf_data["mco"] = {
            "id": workflow.mco.bundle.id,
            "model_data": workflow.mco.__getstate__()
        }

        parameters_data = []
        for param in wf_data["mco"]["model_data"]["parameters"]:  # noqa
            parameters_data.append(
                {
                    "id": param.factory.id,
                    "model_data": param.__getstate__()
                }
            )

        wf_data["mco"]["model_data"]["parameters"] = parameters_data  # noqa

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
