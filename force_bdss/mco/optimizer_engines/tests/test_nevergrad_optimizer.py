from unittest import TestCase, mock
import nevergrad as ng
from nevergrad.instrumentation.transforms import ArctanBound

from force_bdss.api import KPISpecification
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory
from force_bdss.tests.dummy_classes.optimizer_engine import (
    DummyOptimizerEngine,
)
from force_bdss.mco.optimizer_engines.nevergrad_optimizer_engine import (
    NevergradOptimizerEngine,
    NevergradTypeError,
)
from force_bdss.mco.parameters.mco_parameters import (
    FixedMCOParameterFactory,
    RangedMCOParameterFactory,
    ListedMCOParameterFactory,
    CategoricalMCOParameterFactory,
)


class TestNevergradOptimizerEngine(TestCase):
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

        self.optimizer = NevergradOptimizerEngine(
            parameters=self.parameters, kpis=self.kpis
        )

    def test_init(self):
        self.assertIsInstance(self.optimizer, NevergradOptimizerEngine)
        self.assertEqual("Nevergrad", self.optimizer.name)
        self.assertIs(self.optimizer.single_point_evaluator, None)
        self.assertEqual("TwoPointsDE", self.optimizer.algorithms)
        self.assertEqual(500, self.optimizer.budget)

    def test__create_instrumentation_variable(self):
        mock_factory = mock.Mock(
            spec=self.factory,
            plugin_id="pid",
            plugin_name="Plugin",
            id="mcoid",
        )
        fixed_variable = FixedMCOParameterFactory(mock_factory).create_model(
            data_values={"value": 42}
        )
        fixed_variable = self.optimizer._create_instrumentation_variable(
            fixed_variable
        )
        self.assertIsInstance(fixed_variable, ng.var._Constant)
        self.assertEqual(42, fixed_variable.value)

        ranged_variable = RangedMCOParameterFactory(mock_factory).create_model(
            data_values={"lower_bound": -1.0, "upper_bound": 3.14}
        )
        ranged_variable = self.optimizer._create_instrumentation_variable(
            ranged_variable
        )
        self.assertIsInstance(ranged_variable, ng.var.Scalar)
        self.assertEqual(1, len(ranged_variable.transforms))
        self.assertEqual(3.14, ranged_variable.transforms[0].a_max[0])
        self.assertEqual(-1.0, ranged_variable.transforms[0].a_min[0])
        self.assertIsInstance(ranged_variable.transforms[0], ArctanBound)

        listed_variable = ListedMCOParameterFactory(mock_factory).create_model(
            data_values={"levels": [2.0, 1.0, 0.0]}
        )
        listed_variable = self.optimizer._create_instrumentation_variable(
            listed_variable
        )
        self.assertIsInstance(listed_variable, ng.var.OrderedDiscrete)
        self.assertListEqual([0.0, 1.0, 2.0], listed_variable.possibilities)

        categorical_variable = CategoricalMCOParameterFactory(
            mock_factory
        ).create_model(data_values={"categories": ["2.0", "1.0", "0.0"]})
        categorical_variable = self.optimizer._create_instrumentation_variable(
            categorical_variable
        )
        self.assertIsInstance(categorical_variable, ng.var.SoftmaxCategorical)
        self.assertListEqual(
            ["2.0", "1.0", "0.0"], categorical_variable.possibilities
        )

        with self.assertRaises(NevergradTypeError):
            self.optimizer._create_instrumentation_variable(1)

    def test__create_instrumentation(self):
        instrumentation = self.optimizer._assemble_instrumentation()
        self.assertIsInstance(instrumentation, ng.Instrumentation)
        self.assertEqual(
            len(self.optimizer.parameters), len(instrumentation.args)
        )
        for i, parameter in enumerate(self.optimizer.parameters):
            self.assertListEqual(
                [parameter.upper_bound],
                list(instrumentation.args[i].transforms[0].a_max),
            )
            self.assertListEqual(
                [parameter.lower_bound],
                list(instrumentation.args[i].transforms[0].a_min),
            )

    def test__create_kpi_bounds(self):
        self.optimizer.kpis[0].scale_factor = 10
        bounds = self.optimizer.kpi_bounds
        self.assertEqual(len(self.optimizer.kpis), len(bounds))
        for kpi, kpi_bound in zip(self.optimizer.kpis, bounds):
            self.assertEqual(kpi.scale_factor, kpi_bound)
