import sys

from force_bdss.api import (
    BaseMCOCommunicator,
    DataValue)


class DummyDakotaCommunicator(BaseMCOCommunicator):
    def receive_from_mco(self, model):
        data = sys.stdin.read()
        values = list(map(float, data.split()))
        value_names = [p.value_name for p in model.parameters]
        value_types = [p.value_type for p in model.parameters]

        return [
            DataValue(type=type_, name=name, value=value)
            for type_, name, value in zip(
                value_types, value_names, values)]

    def send_to_mco(self, model, kpi_results):
        data = " ".join(
            [" ".join(list(map(str, r.values.tolist()))) for r in kpi_results]
        )
        sys.stdout.write(data)
