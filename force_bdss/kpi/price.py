from traits.api import provides, HasStrictTraits, String

from force_bdss.kpi.i_key_performance_calculator import (
    IKeyPerformanceCalculator)


@provides(IKeyPerformanceCalculator)
class Price(HasStrictTraits):
    computes = String("price")

    def run(self, workflow):
        print("Computing price")
