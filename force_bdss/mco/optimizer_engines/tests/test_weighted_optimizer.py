from unittest import TestCase

from force_bdss.api import (
    KPISpecification,
    RangedMCOParameterFactory,
)
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory
from force_bdss.tests.dummy_classes.optimizer_engine import (
    MixinDummyOptimizerEngine,
)
from force_bdss.mco.optimizer_engines.weighted_optimizer_engine import (
    sen_scaling_method,
)
from force_bdss.mco.optimizer_engines.space_sampling import (
    UniformSpaceSampler,
    DirichletSpaceSampler,
)

from force_bdss.mco.optimizer_engines.weighted_optimizer_engine import (
    WeightedOptimizerEngine
)
from force_bdss.mco.optimizers.scipy_optimizer import ScipyOptimizer


class WeightedScipyEngine(WeightedOptimizerEngine):
    """Provide a ScipyOptimizer instance as the default optimizer
    attribute
    """
    def _optimizer_default(self):
        return ScipyOptimizer()


class DummyOptimizerEngine(MixinDummyOptimizerEngine, WeightedScipyEngine):
    pass


class TestSenScaling(TestCase):
    def setUp(self):
        self.plugin = {"id": "pid", "name": "Plugin"}
        self.factory = DummyMCOFactory(self.plugin)
        self.parameters = [
            RangedMCOParameterFactory(self.factory).create_model(
                {"lower_bound": 0.0, "upper_bound": 1.0}
            )
            for _ in range(4)
        ]
        self.optimizer = DummyOptimizerEngine(parameters=self.parameters)
        self.scaling_values = self.optimizer.scaling_values.tolist()

    def test_sen_scaling(self):
        scaling = sen_scaling_method(
            self.optimizer.dimension, self.optimizer._weighted_optimize
        )
        for computed, reference in zip(scaling, self.scaling_values):
            self.assertAlmostEqual(computed, reference)


class TestWeightedOptimizer(TestCase):
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

        self.optimizer = WeightedScipyEngine(
            parameters=self.parameters, kpis=self.kpis
        )
        self.mocked_optimizer = DummyOptimizerEngine(
            parameters=self.parameters, kpis=self.kpis
        )

    def test_init(self):
        self.assertIsInstance(self.optimizer, WeightedScipyEngine)
        self.assertEqual("Weighted_Optimizer", self.optimizer.name)
        self.assertIs(self.optimizer.single_point_evaluator, None)
        self.assertEqual("SLSQP", self.optimizer.optimizer.algorithms)
        self.assertEqual(7, self.optimizer.num_points)
        self.assertEqual("Uniform", self.optimizer.space_search_mode)

    def test___getstate__(self):
        state = self.optimizer.__getstate__()
        self.assertDictEqual(
            {
                "name": "Weighted_Optimizer",
                "num_points": 7,
                "space_search_mode": "Uniform",
                "verbose_run": False,
                "scaling_method": "sen_scaling_method",
            },
            state,
        )

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
        for i, scaling_factor in enumerate(scaling_factors):
            self.assertAlmostEqual(
                self.mocked_optimizer.scaling_values[i], scaling_factor
            )

    def test_auto_scale(self):
        temp_kpis = [KPISpecification(), KPISpecification(auto_scale=False)]
        self.mocked_optimizer.kpis = temp_kpis
        scaling_factors = self.mocked_optimizer.get_scaling_factors()
        self.assertAlmostEqual(
            self.mocked_optimizer.scaling_values[0], scaling_factors[0]
        )
        self.assertEqual(1.0, scaling_factors[1])

    def test_weighted_score(self):
        self.assertEqual(
            0.0,
            self.mocked_optimizer.weighted_score(
                [1.0] * 4,
                [0.0 for _ in range(self.mocked_optimizer.dimension)],
            ),
        )

        self.assertAlmostEqual(
            0.67 ** 2 + 0.33 ** 2,
            self.mocked_optimizer.weighted_score(
                [1.0] * 4, [1.0] * self.mocked_optimizer.dimension
            ),
        )

    def test__weighted_optimize(self):
        optimal_point, optimal_kpis = self.mocked_optimizer._weighted_optimize(
            [1.0 for _ in range(self.mocked_optimizer.dimension)]
        )
        for kpi in optimal_kpis:
            self.assertAlmostEqual(0.0, kpi)

        self.assertAlmostEqual(0.33, optimal_point[0])
        self.assertAlmostEqual(0.67, optimal_point[1])

    def test_weights_samples(self):
        samples_default = list(self.optimizer.weights_samples())
        for sample in samples_default:
            self.assertAlmostEqual(1.0, sum(sample))

        self.optimizer.space_search_mode = "Dirichlet"
        samples_dirichlet = list(self.optimizer.weights_samples())
        for sample in samples_dirichlet:
            self.assertAlmostEqual(1.0, sum(sample))

        self.assertEqual(len(samples_default), len(samples_default))

    def test_optimize(self):
        for optimal_point, optimal_kpis, _ in self.mocked_optimizer.optimize():
            self.assertAlmostEqual(0.33, optimal_point[0])
            self.assertAlmostEqual(0.67, optimal_point[1])
            for kpi in optimal_kpis:
                self.assertAlmostEqual(0.0, kpi)
