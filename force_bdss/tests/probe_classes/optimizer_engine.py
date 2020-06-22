#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import numpy as np

from traits.api import HasStrictTraits, Array

from force_bdss.local_traits import PositiveInt


class MixinProbeOptimizerEngine(HasStrictTraits):
    #: dummy KPI dimension
    dimension = PositiveInt(2)

    #: known scaling factors to compare with
    scaling_values = Array

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scaling_values = np.array([1./0.17**2] * self.dimension)
