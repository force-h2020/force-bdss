import subprocess
import sys
from traits.api import provides, HasStrictTraits

from force_bdss.i_multi_criteria_optimizers import IMultiCriteriaOptimizer


@provides(IMultiCriteriaOptimizer)
class BasicMultiCriteriaOptimizer(HasStrictTraits):
    def run(self, application):
        print("Basic multicriteria optimizer in action")
        subprocess.check_call([sys.argv[0], "--evaluate",
                               application.workflow_filepath])


