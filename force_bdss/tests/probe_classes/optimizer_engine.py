import numpy as np
from force_bdss.local_traits import PositiveInt
from traits.has_traits import HasStrictTraits
from traits.trait_numeric import Array


class MixinProbeOptimizerEngine(HasStrictTraits):
    #: dummy KPI dimension
    dimension = PositiveInt(2)

    #: known scaling factors to compare with
    scaling_values = Array

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scaling_values = np.array([1./0.17**2] * self.dimension)

    def _score(self, input_point):
        score = (input_point[0] - 0.33) ** 2, (input_point[1] - 0.67) ** 2
        return score