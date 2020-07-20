#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase

from force_bdss.mco.optimizers.scipy_optimizer import (
    ScipyTypeError,
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

    def test_verify_mco_parameters(self):
        optimizer = ScipyOptimizer()
        parameter_factory = self.factory.parameter_factories[0]
        wrong_parameter = parameter_factory.create_model()

        with self.assertRaises(ScipyTypeError):
            optimizer.verify_mco_parameters([wrong_parameter])

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

        # test single-objective (scalar) function
        for point in self.optimizer.optimize_function(
                    lambda arg: arg[0][0]**2 + arg[0][1]**2,
                    params
                ):
            x, y = point[0]
            self.assertAlmostEqual(x, 0.0)
            self.assertAlmostEqual(y, 0.0)

        # test multi-objective function (objectives should be summed)
        for point in self.optimizer.optimize_function(
                    lambda arg: [arg[0][0]**2, arg[0][1]**2],
                    params
                ):
            x, y = point[0]
            self.assertAlmostEqual(x, 0.0)
            self.assertAlmostEqual(y, 0.0)
