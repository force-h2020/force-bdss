import subprocess

import sys

from force_bdss.mco.base_multi_criteria_optimizer import (
    BaseMultiCriteriaOptimizer
)


class DakotaOptimizer(BaseMultiCriteriaOptimizer):
    def run(self):
        print("Running dakota optimizer")
        subprocess.check_call([sys.argv[0], "--evaluate",
                               self.application.workflow_filepath])