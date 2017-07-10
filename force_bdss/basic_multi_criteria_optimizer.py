from traits.api import provides, HasStrictTraits

from force_bdss.i_multi_criteria_optimizers import IMultiCriteriaOptimizer


@provides(IMultiCriteriaOptimizer)
class BasicMultiCriteriaOptimizer(HasStrictTraits):
    def run(self):
        print("Basic multicriteria optimizer in action")
