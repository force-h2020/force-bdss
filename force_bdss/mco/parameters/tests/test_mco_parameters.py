from unittest import TestCase, mock

from traitsui.api import View

from force_bdss.mco.base_mco_factory import BaseMCOFactory
from force_bdss.mco.parameters.mco_parameters import (
    FixedMCOParameter,
    FixedMCOParameterFactory,
    RangedMCOParameter,
    RangedMCOParameterFactory,
    ListedMCOParameter,
    ListedMCOParameterFactory,
    CategoricalMCOParameter,
    CategoricalMCOParameterFactory,
    RangedVectorMCOParameter,
    RangedVectorMCOParameterFactory,
)


class TestFixedMCOParameter(TestCase):
    def setUp(self):
        self.mco_factory = mock.Mock(
            spec=BaseMCOFactory,
            plugin_id="pid",
            plugin_name="Plugin",
            id="mcoid",
        )
        self.factory = FixedMCOParameterFactory(self.mco_factory)
        self.parameter = FixedMCOParameter(self.factory, value=1)

    def test_level(self):
        self.assertEqual(1, self.parameter.value)

    def test_sample_values(self):
        self.assertEqual([1], self.parameter.sample_values)
        self.parameter.value = "something different"
        self.assertEqual(["something different"], self.parameter.sample_values)

    def test_factory(self):
        self.assertEqual("fixed", self.factory.get_identifier())
        self.assertEqual("Fixed", self.factory.get_name())
        self.assertEqual(
            "A parameter with a fixed ReadOnly value.",
            self.factory.get_description(),
        )


class TestRangedMCOParameter(TestCase):
    def setUp(self):
        self.mco_factory = mock.Mock(
            spec=BaseMCOFactory,
            plugin_id="pid",
            plugin_name="Plugin",
            id="mcoid",
        )
        self.factory = RangedMCOParameterFactory(self.mco_factory)
        self.parameter = RangedMCOParameter(self.factory)

    def test_default(self):
        self.assertEqual(0.1, self.parameter.lower_bound)
        self.assertEqual(100.0, self.parameter.upper_bound)
        self.assertEqual(5, self.parameter.n_samples)
        self.assertEqual(50.05, self.parameter.initial_value)
        self.assertIsInstance(self.parameter.default_traits_view(), View)

    def test_sample_values(self):
        for expected, actual in zip(
            [0.1, 25.075, 50.05, 75.025, 100.0],
            list(self.parameter.sample_values),
        ):
            self.assertAlmostEqual(expected, actual)
        self.parameter.lower_bound = 90.0
        for expected, actual in zip(
            [90.0, 92.5, 95.0, 97.5, 100.0], list(self.parameter.sample_values)
        ):
            self.assertAlmostEqual(expected, actual)
        self.parameter.n_samples = 3
        for expected, actual in zip(
            [90.0, 95.0, 100.0], list(self.parameter.sample_values)
        ):
            self.assertAlmostEqual(expected, actual)

    def test_factory(self):
        self.assertEqual("ranged", self.factory.get_identifier())
        self.assertEqual("Ranged", self.factory.get_name())
        self.assertEqual(
            "A parameter with a ranged level in floating point values.",
            self.factory.get_description(),
        )

    def test_custom_ranged_parameter(self):
        parameter = RangedMCOParameter(self.factory, lower_bound=10)
        self.assertEqual(10, parameter.lower_bound)
        self.assertEqual(100.0, parameter.upper_bound)
        self.assertEqual(5, parameter.n_samples)
        self.assertEqual(55.0, parameter.initial_value)

        parameter = RangedMCOParameter(
            self.factory, lower_bound=10, initial_value=100
        )
        self.assertEqual(10, parameter.lower_bound)
        self.assertEqual(100.0, parameter.upper_bound)
        self.assertEqual(5, parameter.n_samples)
        self.assertEqual(100.0, parameter.initial_value)

    def test_verify(self):
        parameter = RangedMCOParameter(
            self.factory,
            lower_bound=10,
            upper_bound=20,
            initial_value=30,
            name="name",
            type="type",
        )
        errors = parameter.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(1, len(messages))
        expected_message = (
            "Initial value of the Ranged parameter must be "
            "within the lower and the upper bounds."
        )
        self.assertEqual(expected_message, messages[0])

        parameter.initial_value = 0
        errors = parameter.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(1, len(messages))
        expected_message = (
            "Initial value of the Ranged parameter must be "
            "within the lower and the upper bounds."
        )
        self.assertEqual(expected_message, messages[0])

        parameter.initial_value = 15
        errors = parameter.verify()
        self.assertEqual(0, len(errors))

        parameter.lower_bound = 25
        errors = parameter.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(2, len(messages))
        expected_message = (
            "Upper bound value of the Ranged parameter must be greater "
            "than the lower bound value."
        )
        self.assertEqual(expected_message, messages[1])


class TestRangedVectorMCOParameter(TestCase):
    def setUp(self):
        self.mco_factory = mock.Mock(
            spec=BaseMCOFactory,
            plugin_id="pid",
            plugin_name="Plugin",
            id="mcoid",
        )
        self.factory = RangedVectorMCOParameterFactory(self.mco_factory)
        self.parameter = RangedVectorMCOParameter(self.factory)

    def test_factory(self):
        self.assertEqual("ranged_vector", self.factory.get_identifier())
        self.assertEqual("Ranged Vector", self.factory.get_name())
        self.assertEqual(
            "A vector parameter with a ranged level in floating point values.",
            self.factory.get_description(),
        )

    def test_default(self):
        self.assertEqual([0.1], self.parameter.lower_bound)
        self.assertEqual([100.0], self.parameter.upper_bound)
        self.assertEqual(5, self.parameter.n_samples)
        self.assertEqual([50.05], self.parameter.initial_value)
        self.assertIsInstance(self.parameter.default_traits_view(), View)

    def test_sample_values(self):
        for expected, actual in zip(
            [0.1, 25.075, 50.05, 75.025, 100.0],
            list(self.parameter.sample_values[0]),
        ):
            self.assertAlmostEqual(expected, actual)
        self.parameter.lower_bound[0] = 90.0
        for expected, actual in zip(
            [90.0, 92.5, 95.0, 97.5, 100.0],
            list(self.parameter.sample_values[0]),
        ):
            self.assertAlmostEqual(expected, actual)
        self.parameter.n_samples = 3
        for expected, actual in zip(
            [90.0, 95.0, 100.0], list(self.parameter.sample_values[0])
        ):
            self.assertAlmostEqual(expected, actual)

    def test_custom_parameter(self):
        parameter = RangedVectorMCOParameter(self.factory, lower_bound=[10])
        self.assertListEqual([10], parameter.lower_bound)
        self.assertListEqual([100.0], parameter.upper_bound)
        self.assertEqual(5, parameter.n_samples)
        self.assertEqual([55.0], parameter.initial_value)

        parameter = RangedVectorMCOParameter(
            self.factory, lower_bound=[10], initial_value=[100]
        )
        self.assertEqual([10], parameter.lower_bound)
        self.assertEqual([100.0], parameter.upper_bound)
        self.assertEqual(5, parameter.n_samples)
        self.assertEqual([100.0], parameter.initial_value)

    def test_dimension_change(self):
        self.assertEqual(1, self.parameter.dimension)
        self.assertEqual(1, len(self.parameter.upper_bound))
        self.assertEqual(1, len(self.parameter.lower_bound))
        self.assertEqual(1, len(self.parameter.initial_value))

        self.parameter.dimension = 3
        self.assertEqual(3, self.parameter.dimension)
        self.assertEqual(3, len(self.parameter.upper_bound))
        self.assertEqual(3, len(self.parameter.lower_bound))
        self.assertEqual(3, len(self.parameter.initial_value))
        self.assertListEqual([0.0, 0.0], self.parameter.upper_bound[1:])
        self.assertListEqual([0.0, 0.0], self.parameter.lower_bound[1:])
        self.assertListEqual([0.0, 0.0], self.parameter.initial_value[1:])

        self.parameter.dimension = 2
        self.assertEqual(2, self.parameter.dimension)
        self.assertEqual(2, len(self.parameter.upper_bound))
        self.assertEqual(2, len(self.parameter.lower_bound))
        self.assertEqual(2, len(self.parameter.initial_value))
        self.assertListEqual([0.0], self.parameter.upper_bound[1:])
        self.assertListEqual([0.0], self.parameter.lower_bound[1:])
        self.assertListEqual([0.0], self.parameter.initial_value[1:])

    def test_verify(self):

        parameter = RangedVectorMCOParameter(
            self.factory,
            lower_bound=[10, 20],
            upper_bound=[20],
            initial_value=[30],
            name="name",
            type="type",
        )

        errors = parameter.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(2, len(messages))

        expected_message = (
            'List attribute lower_bound must possess same length as '
            'determined by dimension attribute: 1')
        self.assertEqual(expected_message, messages[0])

        expected_message = (
            "Initial values at indices [0] of the Ranged Vector parameter "
            "must be within the lower and the upper bounds."
        )
        self.assertEqual(expected_message, messages[1])

        parameter.lower_bound[:] = parameter.lower_bound[:1]
        parameter.initial_value = [0]

        errors = parameter.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(1, len(messages))
        expected_message = (
            "Initial values at indices [0] of the Ranged Vector parameter "
            "must be within the lower and the upper bounds."
        )
        self.assertEqual(expected_message, messages[0])

        parameter.initial_value = [15]
        errors = parameter.verify()
        self.assertEqual(0, len(errors))

        parameter.upper_bound = [7]
        errors = parameter.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(2, len(messages))
        expected_message = (
            "Upper bound values at indices [0] of the Ranged Vector"
            " parameter must greater than the lower bound values."
        )
        self.assertEqual(expected_message, messages[1])


class TestListedMCOParameter(TestCase):
    def setUp(self):
        self.mco_factory = mock.Mock(
            spec=BaseMCOFactory,
            plugin_id="pid",
            plugin_name="Plugin",
            id="mcoid",
        )
        self.factory = ListedMCOParameterFactory(self.mco_factory)
        self.parameter = ListedMCOParameter(self.factory)
        self.filled_parameter = ListedMCOParameter(
            self.factory, levels=[4, 0.0, 2]
        )

    def test_init(self):
        self.assertListEqual([0.0], self.parameter.levels)
        self.assertListEqual([4, 0.0, 2], self.filled_parameter.levels)

    def test_sample_values(self):
        self.assertListEqual([0.0], self.parameter.sample_values)
        self.parameter.levels = [1, 2, 3]
        self.assertListEqual([1, 2, 3], self.parameter.sample_values)

        self.assertListEqual([0.0, 2, 4], self.filled_parameter.sample_values)

    def test_factory(self):
        self.assertEqual("listed", self.factory.get_identifier())
        self.assertEqual("Listed", self.factory.get_name())
        self.assertEqual(
            "A parameter with a listed set of levels"
            " in floating point values.",
            self.factory.get_description(),
        )


class TestCategoricalMCOParameter(TestCase):
    def setUp(self):
        self.mco_factory = mock.Mock(
            spec=BaseMCOFactory,
            plugin_id="pid",
            plugin_name="Plugin",
            id="mcoid",
        )
        self.factory = CategoricalMCOParameterFactory(self.mco_factory)
        self.default_categories = ["chemical1", "chemical2"]
        self.parameter = CategoricalMCOParameter(
            self.factory, categories=self.default_categories
        )

    def test_default(self):
        self.assertListEqual(
            self.default_categories, self.parameter.categories
        )

    def test_sample_values(self):
        self.assertListEqual(
            self.default_categories, self.parameter.sample_values
        )
        self.parameter.categories.append("new_chemical")
        self.assertListEqual(
            self.default_categories + ["new_chemical"],
            self.parameter.sample_values,
        )

    def test_factory(self):
        self.assertEqual("category", self.factory.get_identifier())
        self.assertEqual("Categorical", self.factory.get_name())
        self.assertEqual(
            "A Categorical parameter defining unordered discrete objects.",
            self.factory.get_description(),
        )
