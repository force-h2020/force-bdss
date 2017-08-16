import subprocess
import sys
import itertools
import collections

from force_bdss.api import BaseMCO


def rotated_range(start, stop, starting_value):
    r = list(range(start, stop))
    start_idx = r.index(starting_value)
    d = collections.deque(r)
    d.rotate(-start_idx)
    return list(d)


class DummyDakotaOptimizer(BaseMCO):
    def run(self, model):
        parameters = model.parameters

        values = []
        for p in parameters:
            values.append(
                rotated_range(int(p.lower_bound),
                              int(p.upper_bound),
                              int(p.initial_value))
            )

        value_iterator = itertools.product(*values)

        application = self.factory.plugin.application

        for value in value_iterator:
            ps = subprocess.Popen(
                [sys.argv[0],
                 "--evaluate",
                 application.workflow_filepath],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE)

            out = ps.communicate(
                " ".join([str(v) for v in value]).encode("utf-8"))
            out_data = out[0].decode("utf-8").split()
            self.new_data = {
                'input': tuple(value),
                'output': tuple(out_data)
            }
