from unittest import TestCase

from force_bdss.mco.optimizers.scipy_optimizer import (
    ScipyOptimizer
)


class TestScipyOptimizer(TestCase):

    def setUp(self):
        self.optimizer = ScipyOptimizer()

    def test_init(self):
        self.assertEqual("SLSQP", self.optimizer.algorithms)

    def test_optimize_function(self):
        x, y = self.optimizer.optimize_function(
            lambda arg: arg[0]**2 + arg[1]**2,
            [1, 1],
            [(-2, 2), (-2, 2)]
        )
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 0.0)
