import sys
import numpy

from force_bdss.api import DataSourceParameters, BaseMCOCommunicator


class DakotaCommunicator(BaseMCOCommunicator):
    def receive_from_mco(self):
        data = sys.stdin.read()
        values = list(map(float, data.split()))

        parameters = self.model.parameters

        if len(values) != len(parameters):
            raise ValueError(
                "The passed information length is {}, "
                "but the model specifies {} values.".format(
                    len(values), len(parameters)
                ))

        value_types = [p.value_type for p in parameters]
        value_names = [p.value_name for p in parameters]

        return DataSourceParameters(
            value_names=value_names,
            value_types=value_types,
            values=numpy.array(values)
        )

    def send_to_mco(self, kpi_results):
        data = " ".join(
            [" ".join(list(map(str, r.values.tolist()))) for r in kpi_results]
        )
        sys.stdout.write(data)
