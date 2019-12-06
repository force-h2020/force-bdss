from unittest import TestCase, mock

from traits.api import TraitError

from force_bdss.mco.parameters.mco_parameters import (
    FixedMCOParameter,
    FixedMCOParameterFactory,
    RangedMCOParameter,
    RangedMCOParameterFactory,
    ListedMCOParameter,
    ListedMCOParameterFactory,
    CategoricalMCOParameter,
    CategoricalMCOParameterFactory,
)


class TestFixedMCOParameter(TestCase):
    def setUp(self):
        self.parameter = FixedMCOParameter(
            mock.Mock(spec=FixedMCOParameterFactory), value=1
        )

    def test_level(self):
        self.assertEqual(1, self.parameter.value)

    def test_sample_values(self):
        self.assertEqual([1], self.parameter.sample_values)
        with self.assertRaises(TraitError):
            self.parameter.value = 1


class TestRangedMCOParameter(TestCase):
    def setUp(self):
        self.parameter = RangedMCOParameter(
            mock.Mock(spec=RangedMCOParameterFactory)
        )

    def test_default(self):
        self.assertEqual(0.1, self.parameter.lower_bound)
        self.assertEqual(100.0, self.parameter.upper_bound)
        self.assertEqual(5, self.parameter.n_samples)

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


class TestListedMCOParameter(TestCase):
    def setUp(self):
        self.parameter = ListedMCOParameter(
            mock.Mock(spec=ListedMCOParameterFactory)
        )
        self.filled_parameter = ListedMCOParameter(
            mock.Mock(spec=ListedMCOParameterFactory), levels=[4, 0.0, 2]
        )

    def test_init(self):
        self.assertListEqual([0.0], self.parameter.levels)
        self.assertListEqual([4, 0.0, 2], self.filled_parameter.levels)

    def test_sample_values(self):
        self.assertListEqual([0.0], self.parameter.sample_values)
        self.parameter.levels = [1, 2, 3]
        self.assertListEqual([1, 2, 3], self.parameter.sample_values)

        self.assertListEqual([0.0, 2, 4], self.filled_parameter.sample_values)


class TestCategoricalMCOParameter(TestCase):
    def setUp(self):
        self.default_categories = ["chemical1", "chemical2"]
        self.parameter = CategoricalMCOParameter(
            mock.Mock(spec=CategoricalMCOParameterFactory),
            categories=self.default_categories,
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
