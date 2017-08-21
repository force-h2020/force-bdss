from force_bdss.api import BaseDataSource, DataValue
from force_bdss.core.slot import Slot


class CodeEditorDataSource(BaseDataSource):
    def run(self, model, parameters):
        outputs = [DataValue(type="PRESSURE", value=0)]
        exec(
            model.code,
            {'inputs': parameters, 'outputs': outputs}
        )
        return outputs

    def slots(self, model):
        return (
            (
                Slot(type="PRESSURE"),
            ),
            (
                Slot(type="PRESSURE"),
            )
        )
