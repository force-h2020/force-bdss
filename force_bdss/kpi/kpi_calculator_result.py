from traits.api import HasTraits, List, Array, ArrayOrNone, String, Instance

from .base_kpi_calculator import BaseKPICalculator


class KPICalculatorResult(HasTraits):
    originator = Instance(BaseKPICalculator)
    value_names = List(String)
    value_types = List(String)
    values = Array(shape=(None, ))
    accuracy = ArrayOrNone(shape=(None, ))
    quality = ArrayOrNone(shape=(None, ))

    def __str__(self):
        return """
        DataSourceResults

        originator:
        {}

        value_names:
        {}

        value_types:
        {}

        values:
        {}

        Accuracy:
        {}

        Quality:
        {}
        """.format(
                self.originator,
                self.value_names,
                self.value_types,
                self.values,
                self.accuracy,
                self.quality)
