from traits.api import HasTraits, Array, ArrayOrNone, List, String, Instance

from .base_data_source import BaseDataSource


class DataSourceResult(HasTraits):
    """Represents the result of a simulator.
    It contains the resulting cuba key, the associated uncertainty and the
    originating simulator.
    Difference between uncertainty and quality: uncertainty is a numerical value
    of the value, as in the case of an experimental simulation.
    quality is the level of accuracy of the (e.g.c omputational) method, as
    the importance and reliability of that value. It should be an enumeration
    value such as HIGH, MEDIUM, POOR"""
    originator = Instance(BaseDataSource)
    value_types = List(String)
    values = Array(shape=(None, None))
    accuracy = ArrayOrNone(shape=(None, None))
    quality = ArrayOrNone(shape=(None, None))
