import sys
import numpy

from force_bdss.api import DataSourceParameters, BaseMCOCommunicator


class DummyDakotaCommunicator(BaseMCOCommunicator):
    def receive_from_mco(self):
        data = sys.stdin.read()
        values = list(map(float, data.split()))
        return DataSourceParameters(
            value_types=["DUMMY"]*len(values),
            values=numpy.array(values)
        )


    def send_to_mco(self, kpi_results):
        data = " ".join(
            [" ".join(list(map(str, r.values.tolist()))) for r in kpi_results]
        )
        sys.stdout.write(data)
