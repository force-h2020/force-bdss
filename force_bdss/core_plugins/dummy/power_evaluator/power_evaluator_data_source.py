import math

from force_bdss.api import BaseDataSource, DataValue
from force_bdss.core.slot import Slot


class PowerEvaluatorDataSource(BaseDataSource):
    def run(self, model, parameters):
        x = parameters[0].value
        return [
            DataValue(
                type=model.cuba_type_out,
                value=math.pow(x, model.power)
            )]

    def slots(self, model):
        return (
            (
                Slot(type=model.cuba_type_in),
            ),
            (
                Slot(type=model.cuba_type_out),
            )
        )
