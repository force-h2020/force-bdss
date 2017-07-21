import subprocess

import sys

from force_bdss.api import BaseMultiCriteriaOptimizer


class DummyDakotaOptimizer(BaseMultiCriteriaOptimizer):
    def run(self):
        print("Running dakota optimizer")
        for initial_value in range(10):
            ps = subprocess.Popen(
                [sys.argv[0],
                 "--evaluate",
                 self.application.workflow_filepath],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE)

            out = ps.communicate("{}".format(initial_value).encode("utf-8"))
            print("{}: {}".format(initial_value, out[0].decode("utf-8")))


