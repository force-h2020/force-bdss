#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import numpy as np

from traits.api import Array, HasStrictTraits

from force_bdss.api import PositiveInt, BaseOptimizerEngine


class EmptyOptimizerEngine(BaseOptimizerEngine):
    def optimize(self):
        return [0.0]


class MixinDummyOptimizerEngine(HasStrictTraits):
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
