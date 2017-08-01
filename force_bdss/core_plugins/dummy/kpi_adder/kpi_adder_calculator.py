from force_bdss.api import BaseKPICalculator, DataValue
from force_bdss.core.slot import Slot


class KPIAdderCalculator(BaseKPICalculator):
    def run(self, model, data_source_results):
        sum = 0.0

        for res in data_source_results:
            if res.type != model.cuba_type_in:
                continue

            sum += res.value

        return [
            DataValue(
                type=model.cuba_type_out,
                value=sum
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
