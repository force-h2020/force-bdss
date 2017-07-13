import subprocess

import sys

from traits.api import provides, HasStrictTraits, String

from force_bdss.mco.i_multi_criteria_optimizers import IMultiCriteriaOptimizer


@provides(IMultiCriteriaOptimizer)
class Dakota(HasStrictTraits):
    name = String("dakota")

    def run(self, application):
        print("Running dakota optimizer")
        subprocess.check_call([sys.argv[0], "--evaluate",
                               application.workflow_filepath])
