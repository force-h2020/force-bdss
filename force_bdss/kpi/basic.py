from traits.api import provides, HasStrictTraits, String

from force_bdss.kpi.i_key_performance_calculator import (
    IKeyPerformanceCalculator)


@provides(IKeyPerformanceCalculator)
class Basic(HasStrictTraits):
    computes = String("basic")

    def run(self, workflow):
        print("Computing basic key performance indicator, {}".format(workflow))
