from traits.api import HasTraits, Array, ArrayOrNone, List, String, Instance

from .base_data_source import BaseDataSource


class DataSourceResult(HasTraits):
    """Represents the result of a simulator.
    It contains the resulting cuba key, the associated uncertainty and the
    originating simulator.
    Difference between uncertainty and quality: uncertainty is a numerical
    value of the value, as in the case of an experimental simulation.
    quality is the level of accuracy of the (e.g. computational) method, as
    the importance and reliability of that value. It should be an enumeration
    value such as HIGH, MEDIUM, POOR"""
    originator = Instance(BaseDataSource)
    value_names = List(String)
    value_types = List(String)
    values = Array(shape=(None, None))
    accuracy = ArrayOrNone(shape=(None, None))
    quality = ArrayOrNone(shape=(None, None))

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
