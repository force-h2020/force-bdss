import sys
import numpy

from force_bdss.api import DataSourceParameters, BaseMCOCommunicator


class DakotaCommunicator(BaseMCOCommunicator):
    def receive_from_mco(self):
        data = sys.stdin.read()
        values = list(map(float, data.split()))

        value_types = self.model.value_types
        if len(values) != len(value_types):
            raise ValueError("Length of provided data differs from the number "
                             "of expected types. {} {}".format(values,
                                                               value_types))

        return DataSourceParameters(
            value_types=value_types,
            values=numpy.array(values)
        )

    def send_to_mco(self, kpi_results):
        data = " ".join(
            [" ".join(list(map(str, r.values.tolist()))) for r in kpi_results]
        )
        sys.stdout.write(data)
