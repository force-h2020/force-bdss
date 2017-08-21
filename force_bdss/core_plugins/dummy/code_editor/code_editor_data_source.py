import copy

from force_bdss.api import BaseDataSource, DataValue
from force_bdss.core.slot import Slot


class CodeEditorDataSource(BaseDataSource):
    def run(self, model, parameters):
        environment = {param.name: copy.deepcopy(param.value)
                       for param in parameters}
        exec(
            model.code,
            environment
        )

        return [DataValue(type="PRESSURE", value=environment[output_name])
                for output_name in model.output_slot_names]

    def slots(self, model):
        return (
            tuple(Slot(type="PRESSURE") for _ in range(model.nb_inputs)),
            tuple(Slot(type="PRESSURE") for _ in range(model.nb_outputs))
        )
