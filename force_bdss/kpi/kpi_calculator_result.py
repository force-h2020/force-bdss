from traits.api import HasTraits, List, Array, ArrayOrNone, String, Instance

from .base_kpi_calculator import BaseKPICalculator


class KPICalculatorResult(HasTraits):
    originator = Instance(BaseKPICalculator)
    value_types = List(String)
    values = Array(shape=(None, ))
    accuracy = ArrayOrNone(shape=(None, ))
    quality = ArrayOrNone(shape=(None, ))
