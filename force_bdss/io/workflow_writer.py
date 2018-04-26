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
        data = dict(version="1")

        data["workflow"] = self._workflow_data(workflow)
        json.dump(data, f, indent=4)

    def _workflow_data(self, workflow):
        workflow_data = {
            "mco": self._mco_data(workflow.mco),
            "kpi_calculators": [
                self._model_data(kpic)
                for kpic in workflow.kpi_calculators],
            "execution_layers": [
                self._execution_layer_data(el)
                for el in workflow.execution_layers],
            "notification_listeners": [
                self._model_data(nl)
                for nl in workflow.notification_listeners
            ]
        }

        return workflow_data

    def _mco_data(self, mco):
        """Extracts the data from the MCO object and returns its dictionary.
        If the MCO is None, returns None"""
        if mco is None:
            return None

        data = self._model_data(mco)

        parameters_data = []
        for param in data["model_data"]["parameters"]:
            state = param.__getstate__()
            try:
                state.pop("__traits_version__")
            except KeyError:
                pass

            parameters_data.append(
                {
                    "id": param.factory.id,
                    "model_data": state
                }
            )

        data["model_data"]["parameters"] = parameters_data
        return data

    def _execution_layer_data(self, layer):
        """Extracts the execution layer list of DataSource models"""
        data = []

        for ds in layer:
            data.append(self._model_data(ds))

        return data

    def _model_data(self, model):
        """
        Extracts the data from an external model and returns its dictionary
        """
        state = model.__getstate__()
        try:
            state.pop("__traits_version__")
        except KeyError:
            pass

        return {
            "id": model.factory.id,
            "model_data": state
        }
