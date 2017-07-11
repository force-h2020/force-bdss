from traits.api import provides, HasStrictTraits

from force_bdss.kpi.i_key_performance_calculator import IKeyPerformanceCalculator


@provides(IKeyPerformanceCalculator)
class BasicKeyPerformanceCalculator(HasStrictTraits):
    def run(self, workflow):
        print("Computing basic key performance indicator, {}".format(workflow))
