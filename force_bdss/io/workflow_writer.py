import json
from traits.api import HasStrictTraits
from collections import Iterable


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
            state = traits_to_dict(param)

            parameters_data.append(
                {
                    "id": param.factory.id,
                    "model_data": state
                }
            )

        data["model_data"]["parameters"] = parameters_data

        kpis_data = []
        for kpi in data["model_data"]["kpis"]:
            kpis_data.append(
                traits_to_dict(kpi)
            )

        data["model_data"]["kpis"] = kpis_data

        return data

    def _execution_layer_data(self, layer):
        """Extracts the execution layer list of DataSource models"""
        data = []

        for ds in layer.data_sources:
            data.append(self._model_data(ds))

        return data

    def _model_data(self, model):
        """
        Extracts the data from an external model and returns its dictionary
        """
        state = traits_to_dict(model)

        return {
            "id": model.factory.id,
            "model_data": state
        }


def traits_to_dict(traits_obj):
    """Converts a traits class into a dict, removing the pesky
    traits version."""

    state = traits_obj.__getstate__()

    state = pop_recursive(state, '__traits_version__')

    return state


def pop_recursive(dictionary, remove_key):
    """Recursively remove a named key from dictionary and any contained
    dictionaries."""
    try:
        dictionary.pop(remove_key)
    except KeyError:
        pass

    for key,value in dictionary.items():
        # If remove_key is in the dict, remove it
        if isinstance(value, dict):
            pop_recursive(value, remove_key)
        # If we have a non-dict iterable which contains a dict,
        # call pop.(remove_key) from that as well
        elif isinstance(value, (tuple, list)):
            for element in value:
                if isinstance(element, dict):
                    pop_recursive(element, remove_key)

    return dictionary
