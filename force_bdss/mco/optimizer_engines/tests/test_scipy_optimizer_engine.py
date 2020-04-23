from unittest import TestCase

from force_bdss.api import (
    KPISpecification,
    ScipyOptimizerEngine,
    RangedMCOParameterFactory,
)
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory
from force_bdss.tests.dummy_classes.optimizer_engine import (
    MixinDummyOptimizerEngine,
)


class DummyOptimizerEngine(MixinDummyOptimizerEngine, ScipyOptimizerEngine):
    pass


class TestWeightedOptimizer(TestCase):
    def setUp(self):
        self.plugin = {"id": "pid", "name": "Plugin"}
        self.factory = DummyMCOFactory(self.plugin)

        self.kpis = [KPISpecification(), KPISpecification()]
        self.parameters = [1, 1, 1, 1]

        self.kpis = self.kpis

        self.parameters = [
            RangedMCOParameterFactory(self.factory).create_model(
                {"lower_bound": 0.0, "upper_bound": 1.0}
            )
            for _ in self.parameters
        ]

        self.optimizer = ScipyOptimizerEngine(
            parameters=self.parameters, kpis=self.kpis
        )
        self.mocked_optimizer = DummyOptimizerEngine(
            parameters=self.parameters, kpis=self.kpis
        )

    def test_init(self):
        self.assertIsInstance(self.optimizer, ScipyOptimizerEngine)
        self.assertEqual("Scipy_Optimizer", self.optimizer.name)
        self.assertIs(self.optimizer.single_point_evaluator, None)
        self.assertEqual("SLSQP", self.optimizer.algorithms)

        self.assertListEqual(
            self.optimizer.initial_parameter_value,
            [0.5] * len(self.parameters),
        )
        self.assertListEqual(
            self.optimizer.parameter_bounds,
            [(0.0, 1.0)] * len(self.parameters),
        )

    def test___getstate__(self):
        state = self.optimizer.__getstate__()
        self.assertDictEqual(
            {
                "name": "Scipy_Optimizer",
                "algorithms": "SLSQP",
                "verbose_run": False,
            },
            state,
        )

    def test_optimize(self):
        for optimal_point, optimal_kpis, _ in self.mocked_optimizer.optimize():
            self.assertAlmostEqual(0.33, optimal_point[0])
            self.assertAlmostEqual(0.67, optimal_point[1])
            for kpi in optimal_kpis:
                self.assertAlmostEqual(0.0, kpi)
