import subprocess
import sys

from traits.api import provides, HasStrictTraits, String

from force_bdss.mco.i_multi_criteria_optimizers import IMultiCriteriaOptimizer


@provides(IMultiCriteriaOptimizer)
class Basic(HasStrictTraits):
    name = String("basic")

    def run(self, application):
        print("Running Basic optimizer")
        subprocess.check_call([sys.argv[0], "--evaluate",
                               application.workflow_filepath])
