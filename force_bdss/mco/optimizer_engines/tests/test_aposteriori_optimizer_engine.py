from unittest import TestCase

from force_bdss.api import (
    KPISpecification,
    RangedMCOParameterFactory,
)
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory
from force_bdss.tests.dummy_classes.optimizer_engine import (
    MixinDummyOptimizerEngine
)

from force_bdss.mco.optimizer_engines.aposteriori_optimizer_engine import (
    AposterioriOptimizerEngine
)
from force_bdss.mco.optimizers.scipy_optimizer import (
    ScipyOptimizer
)


class AposterioriScipyEngine(AposterioriOptimizerEngine):
    """Provide a ScipyOptimizer instance as the default optimizer
    attribute
    """
    def _optimizer_default(self):
        return ScipyOptimizer()


class DummyOptimizerEngine(MixinDummyOptimizerEngine, AposterioriScipyEngine):
    pass


class TestAposterioriEngine(TestCase):

    def setUp(self):
        self.plugin = {"id": "pid", "name": "Plugin"}
        self.factory = DummyMCOFactory(self.plugin)

        self.kpis = [KPISpecification(), KPISpecification()]
        self.parameters = [1, 1, 1, 1]

        self.parameters = [
            RangedMCOParameterFactory(self.factory).create_model(
                {"lower_bound": 0.0, "upper_bound": 1.0}
            )
            for _ in self.parameters
        ]

        self.optimizer = AposterioriScipyEngine(
            parameters=self.parameters, kpis=self.kpis
        )
        self.mocked_optimizer = DummyOptimizerEngine(
            parameters=self.parameters, kpis=self.kpis
        )

    def test_init(self):
        self.assertIsInstance(self.optimizer, AposterioriScipyEngine)
        self.assertEqual("APosteriori_Optimizer", self.optimizer.name)
        self.assertIs(self.optimizer.single_point_evaluator, None)
        self.assertIsInstance(self.optimizer.optimizer, ScipyOptimizer)
        self.assertEqual("SLSQP", self.optimizer.optimizer.algorithms)

    def test___getstate__(self):
        state = self.optimizer.__getstate__()
        self.assertDictEqual(
            {
                "name": "APosteriori_Optimizer",
                "verbose_run": False
            },
            state,
        )

    def test_optimize(self):
        """ To test this we need an a posteriori optimizer installed in bdss.
        """
        # NOTE: we can use a dummy IOptimize class here to check the
        # values that should be returned from calling
        # AposterioriOptimizerEngine.optimize
