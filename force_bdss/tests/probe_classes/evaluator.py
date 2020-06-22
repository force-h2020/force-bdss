#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import (
    provides,
    Instance
)

from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.mco.i_evaluator import IEvaluator


class DummyMCOModel(BaseMCOModel):
    pass


@provides(IEvaluator)
class ProbeEvaluator:

    mco_model = Instance(DummyMCOModel)

    def evaluate(self, parameter_values):
        return [1.0, 1.0]


@provides(IEvaluator)
class GaussProbeEvaluator:

    def evaluate(self, input_point):
        return (input_point[0] - 0.33) ** 2, (input_point[1] - 0.67) ** 2
