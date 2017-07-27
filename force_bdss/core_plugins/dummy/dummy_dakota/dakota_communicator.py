import sys
import numpy

from force_bdss.api import DataSourceParameters, BaseMCOCommunicator


class DummyDakotaCommunicator(BaseMCOCommunicator):
    def receive_from_mco(self, model):
        data = sys.stdin.read()
        values = list(map(float, data.split()))
        value_names = [p.value_name for p in model.parameters]
        value_types = [p.value_type for p in model.parameters]

        return DataSourceParameters(
            value_names=value_names,
            value_types=value_types,
            values=numpy.array(values)
        )

    def send_to_mco(self, model, kpi_results):
        data = " ".join(
            [" ".join(list(map(str, r.values.tolist()))) for r in kpi_results]
        )
        sys.stdout.write(data)
