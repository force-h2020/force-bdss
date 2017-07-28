from traits.api import HasTraits, List, Array, ArrayOrNone, String, Instance

from .base_kpi_calculator import BaseKPICalculator


class KPICalculatorResult(HasTraits):
    """Contains the results from a single KPICalculator evaluation"""

    #: The originating KPI calculator
    originator = Instance(BaseKPICalculator)

    #: The user-attributed names of each computed value
    value_names = List(String)

    #: The CUBA types of each of the computed values
    value_types = List(String)

    #: The values, as a single array of values
    values = Array(shape=(None, ))

    #: If present, the numerical accuracy of the above values.
    accuracy = ArrayOrNone(shape=(None, ))

    #: If present, the quality of the above values.
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
