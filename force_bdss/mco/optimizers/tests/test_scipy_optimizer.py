from unittest import TestCase

from force_bdss.mco.optimizers.scipy_optimizer import (
    ScipyOptimizer
)

from force_bdss.tests.dummy_classes.mco import DummyMCOFactory

from force_bdss.mco.parameters.mco_parameters import (
    RangedVectorMCOParameter,
    RangedVectorMCOParameterFactory
)


class TestScipyOptimizer(TestCase):

    def setUp(self):
        self.optimizer = ScipyOptimizer()

        self.plugin = {"id": "pid", "name": "Plugin"}
        self.factory = DummyMCOFactory(self.plugin)

    def test_init(self):
        self.assertEqual("SLSQP", self.optimizer.algorithms)

    def test_optimize_function(self):

        factory = RangedVectorMCOParameterFactory(self.factory)

        params = [RangedVectorMCOParameter(
            factory=factory,
            name='coordinates',
            dimension=2,
            lower_bound=[-2, -2],
            upper_bound=[2, 2],
            initial_value=[1, 1]
        )]

        for point in self.optimizer.optimize_function(
                    lambda arg: arg[0][0]**2 + arg[0][1]**2,
                    params
                ):
            x, y = point[0]
            self.assertAlmostEqual(x, 0.0)
            self.assertAlmostEqual(y, 0.0)
