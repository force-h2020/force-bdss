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
        }

        data["workflow"] = self._workflow_data(workflow)
        json.dump(data, f)

    def _workflow_data(self, workflow):
        workflow_data = {
            "mco": self._mco_data(workflow.mco),
            "kpi_calculators": [
                self._bundle_model_data(kpic)
                for kpic in workflow.kpi_calculators],
            "data_sources": [
                self._bundle_model_data(ds)
                for ds in workflow.data_sources]
        }

        return workflow_data

    def _mco_data(self, mco):
        """Extracts the data from the MCO object and returns its dictionary.
        If the MCO is None, returns None"""
        if mco is None:
            return None

        data = self._bundle_model_data(mco)

        parameters_data = []
        for param in data["model_data"]["parameters"]:
            parameters_data.append(
                {
                    "id": param.factory.id,
                    "model_data": param.__getstate__()
                }
            )

        data["model_data"]["parameters"] = parameters_data
        return data

    def _bundle_model_data(self, bundle_model):
        """
        Extracts the data from a bundle model and returns its dictionary
        """
        return {
            "id": bundle_model.bundle.id,
            "model_data": bundle_model.__getstate__()
        }
