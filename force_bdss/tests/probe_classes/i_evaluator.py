from traits.api import (
    provides,
    Instance
)

from force_bdss.mco.i_evaluator import IEvaluator

from force_bdss.mco.base_mco_model import BaseMCOModel


class DummyMCOModel(BaseMCOModel):
    pass


@provides(IEvaluator)
class ProbeIEvaluator:

    mco_model = Instance(DummyMCOModel)

    def evaluate(self, parameter_values):
        return [1.0, 1.0]
