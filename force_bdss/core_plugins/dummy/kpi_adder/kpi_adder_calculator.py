import numpy

from force_bdss.api import BaseKPICalculator
from force_bdss.api import KPICalculatorResult


class KPIAdderCalculator(BaseKPICalculator):
    def run(self, data_source_results):
        sum = 0.0
        for res in data_source_results:
            try:
                value_idx = res.value_types.index(self.model.cuba_type_in)
            except ValueError:
                continue

            sum += res.values[value_idx].sum()

        return KPICalculatorResult(
            originator=self,
            value_types=[self.model.cuba_type_out],
            values=numpy.array([sum])
        )
