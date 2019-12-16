from unittest import TestCase

from force_bdss.api import KPISpecification
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory
from force_bdss.tests.dummy_classes.optimizer_engine import (
    DummyOptimizerEngine,
)
from force_bdss.mco.optimizer_engines.weighted_optimizer_engine import (
    sen_scaling_method,
    WeightedOptimizerEngine,
)
from force_bdss.mco.optimizer_engines.utilities import (
    UniformSpaceSampler,
    DirichletSpaceSampler,
)


class MockedWeightedOptimizerEngine(WeightedOptimizerEngine):
    def _weighted_optimize(self, weights):
        dummy_optimizer = DummyOptimizerEngine()
        return dummy_optimizer._weighted_optimize(weights)


class TestSenScaling(TestCase):
    def setUp(self):
        self.optimizer = DummyOptimizerEngine()
        self.scaling_values = self.optimizer.scaling_values.tolist()

    def test_sen_scaling(self):
        scaling = sen_scaling_method(
            self.optimizer.dimension, self.optimizer._weighted_optimize
        )
        self.assertListEqual(scaling.tolist(), self.scaling_values)


class TestWeightedOptimizer(TestCase):
    def setUp(self):
        self.plugin = {"id": "pid", "name": "Plugin"}
        self.factory = DummyMCOFactory(self.plugin)

        self.kpis = [KPISpecification(), KPISpecification()]
        self.parameters = [1, 1, 1, 1]

        self.kpis = self.kpis
        self.parameters = [
            self.factory.parameter_factories[0].create_model()
            for _ in self.parameters
        ]

        self.optimizer = WeightedOptimizerEngine(
            parameters=self.parameters, kpis=self.kpis
        )
        self.mocked_optimizer = MockedWeightedOptimizerEngine(
            parameters=self.parameters, kpis=self.kpis
        )

    def test_init(self):
        self.assertIsInstance(self.optimizer, WeightedOptimizerEngine)
        self.assertEqual("Weighted_Optimizer", self.optimizer.name)
        self.assertIs(self.optimizer.single_point_evaluator, None)
        self.assertEqual("SLSQP", self.optimizer.algorithms)
        self.assertEqual(7, self.optimizer.num_points)
        self.assertEqual("Uniform", self.optimizer.space_search_mode)

    def test__space_search_distribution(self):
        for strategy, klass in (
            ("Uniform", UniformSpaceSampler),
            ("Dirichlet", DirichletSpaceSampler),
            ("Uniform", UniformSpaceSampler),
        ):
            self.optimizer.space_search_mode = strategy
            distribution = self.optimizer._space_search_distribution()
            self.assertIsInstance(distribution, klass)
            self.assertEqual(len(self.kpis), distribution.dimension)
            self.assertEqual(7, distribution.resolution)

    def test_scaling_factors(self):
        scaling_factors = self.mocked_optimizer.get_scaling_factors()
        self.assertEqual([0.1, 0.1], scaling_factors)

    def test_auto_scale(self):
        temp_kpis = [KPISpecification(), KPISpecification(auto_scale=False)]
        self.mocked_optimizer.kpis = temp_kpis
        scaling_factors = self.mocked_optimizer.get_scaling_factors()
        self.assertEqual([0.1, 1.0], scaling_factors)

    def test___getstate__(self):
        state = self.optimizer.__getstate__()
        self.assertDictEqual(
            {
                "name": "Weighted_Optimizer",
                "algorithms": "SLSQP",
                "num_points": 7,
                "space_search_mode": "Uniform",
                "verbose_run": False,
                "scaling_method": "sen_scaling_method"
            },
            state,
        )
