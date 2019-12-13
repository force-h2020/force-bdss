import numpy as np

from traits.api import Array

from force_bdss.api import PositiveInt
from force_bdss.mco.optimizer_engines.base_optimizer_engine import (
    BaseOptimizerEngine,
)


class DummyOptimizerEngine(BaseOptimizerEngine):

    #: dummy optimizer KPI dimension
    dimension = PositiveInt(2)

    #: dispersion of the KPIs
    margins = Array

    #: minimum value of KPIs
    min_values = Array

    #: known scaling factors to compare with
    scaling_values = Array

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.margins = np.array([10.0 for _ in range(self.dimension)])
        self.min_values = np.array([i for i in range(self.dimension)])
        self.scaling_values = np.array([0.1] * self.dimension)

    def optimize(self):
        return [0.0]

    def _weighted_optimize(self, weights):
        return 0, self.min_values + weights * self.margins
