from unittest import TestCase
from force_bdss.mco.optimizer_engines.utilities import (
    convert_by_mask,
    SpaceSampler,
    DirichletSpaceSampler,
    UniformSpaceSampler,
    resolution_to_sample_size,
)


class TestConvertUtil(TestCase):
    def test_convert_by_mask(self):
        kpi_specs = ["MINIMISE", "MAXIMISE"]
        values = [10.0, 20.0]
        inv_values = convert_by_mask(values, kpi_specs)
        self.assertListEqual(list(inv_values), [10.0, -20.0])

        inv_values = convert_by_mask(values, kpi_specs, "MINIMISE")
        self.assertListEqual(list(inv_values), [10.0, -20.0])

        inv_values = convert_by_mask(values, kpi_specs, "MAXIMISE")
        self.assertListEqual(list(inv_values), [-10.0, 20.0])

        inv_values = convert_by_mask(values, kpi_specs, "SOMETHING")
        self.assertListEqual(list(inv_values), [-10.0, -20.0])


class TestSamplesConvert(TestCase):
    def test_convert(self):
        samples_total = resolution_to_sample_size(
            space_dimension=3, n_points=5
        )
        known_samples_total = 15
        self.assertEqual(known_samples_total, samples_total)


class BaseTestSampler(TestCase):
    distribution = SpaceSampler

    def generate_values(self, *args, **kwargs):
        return self.distribution(*args, **kwargs).generate_space_sample(
            **kwargs
        )


class TestDirichletSpaceSampler(BaseTestSampler):
    distribution = DirichletSpaceSampler

    def setUp(self):
        self.dimensions = [3, 1, 5]
        self.alphas = [1, 0.5, 10]
        self.n_points = [3, 10, 6]

    def generate_samplers(self):
        for dimension in self.dimensions:
            for n_points in self.n_points:
                for alpha in self.alphas:
                    yield DirichletSpaceSampler(
                        dimension, n_points, alpha=alpha
                    )

    def test__get_sample_point(self):
        for sampler in self.generate_samplers():
            self.assertAlmostEqual(1.0, sum(sampler._get_sample_point()))

    def test_generate_space_sample(self):
        for sampler in self.generate_samplers():

            space_sample = list(sampler.generate_space_sample())
            self.assertEqual(
                len(space_sample),
                resolution_to_sample_size(
                    sampler.dimension, sampler.resolution
                ),
            )

            for sample in space_sample:
                self.assertAlmostEqual(1.0, sum(sample))


class TestUniformSpaceSampler(BaseTestSampler):
    distribution = UniformSpaceSampler

    def test_space_sample(self):
        self.assertEqual(
            [
                [1.0, 0.0, 0.0],
                [0.75, 0.25, 0.0],
                [0.75, 0.0, 0.25],
                [0.50, 0.50, 0.0],
                [0.50, 0.25, 0.25],
                [0.50, 0.0, 0.50],
                [0.25, 0.75, 0.0],
                [0.25, 0.50, 0.25],
                [0.25, 0.25, 0.50],
                [0.25, 0.0, 0.75],
                [0.0, 1.0, 0.0],
                [0.0, 0.75, 0.25],
                [0.0, 0.50, 0.50],
                [0.0, 0.25, 0.75],
                [0.0, 0.0, 1.0],
            ],
            list(self.generate_values(3, 5, with_zero_values=True)),
        )

        self.assertEqual(
            [[1.0]], list(self.generate_values(1, 5, with_zero_values=True))
        )
        self.assertEqual(
            [[1.0, 0.0], [0.75, 0.25], [0.50, 0.50], [0.25, 0.75], [0.0, 1.0]],
            list(self.generate_values(2, 5, with_zero_values=True)),
        )

        self.assertEqual(
            [
                [1.0, 0.0, 0.0],
                [0.875, 0.125, 0.0],
                [0.875, 0.0, 0.125],
                [0.75, 0.25, 0.0],
                [0.75, 0.125, 0.125],
                [0.75, 0.0, 0.25],
                [0.625, 0.375, 0.0],
                [0.625, 0.25, 0.125],
                [0.625, 0.125, 0.25],
                [0.625, 0.0, 0.375],
                [0.5, 0.5, 0.0],
                [0.5, 0.375, 0.125],
                [0.5, 0.25, 0.25],
                [0.5, 0.125, 0.375],
                [0.5, 0.0, 0.5],
                [0.375, 0.625, 0.0],
                [0.375, 0.5, 0.125],
                [0.375, 0.375, 0.25],
                [0.375, 0.25, 0.375],
                [0.375, 0.125, 0.5],
                [0.375, 0.0, 0.625],
                [0.25, 0.75, 0.0],
                [0.25, 0.625, 0.125],
                [0.25, 0.5, 0.25],
                [0.25, 0.375, 0.375],
                [0.25, 0.25, 0.5],
                [0.25, 0.125, 0.625],
                [0.25, 0.0, 0.75],
                [0.125, 0.875, 0.0],
                [0.125, 0.75, 0.125],
                [0.125, 0.625, 0.25],
                [0.125, 0.5, 0.375],
                [0.125, 0.375, 0.5],
                [0.125, 0.25, 0.625],
                [0.125, 0.125, 0.75],
                [0.125, 0.0, 0.875],
                [0.0, 1.0, 0.0],
                [0.0, 0.875, 0.125],
                [0.0, 0.75, 0.25],
                [0.0, 0.625, 0.375],
                [0.0, 0.5, 0.5],
                [0.0, 0.375, 0.625],
                [0.0, 0.25, 0.75],
                [0.0, 0.125, 0.875],
                [0.0, 0.0, 1.0],
            ],
            list(self.generate_values(3, 9, with_zero_values=True)),
        )

        self.assertEqual(
            [[0.75, 0.25], [0.50, 0.50], [0.25, 0.75]],
            list(self.generate_values(2, 5, with_zero_values=False)),
        )

        self.assertEqual(
            [
                [0.75, 0.125, 0.125],
                [0.625, 0.25, 0.125],
                [0.625, 0.125, 0.25],
                [0.5, 0.375, 0.125],
                [0.5, 0.25, 0.25],
                [0.5, 0.125, 0.375],
                [0.375, 0.5, 0.125],
                [0.375, 0.375, 0.25],
                [0.375, 0.25, 0.375],
                [0.375, 0.125, 0.5],
                [0.25, 0.625, 0.125],
                [0.25, 0.5, 0.25],
                [0.25, 0.375, 0.375],
                [0.25, 0.25, 0.5],
                [0.25, 0.125, 0.625],
                [0.125, 0.75, 0.125],
                [0.125, 0.625, 0.25],
                [0.125, 0.5, 0.375],
                [0.125, 0.375, 0.5],
                [0.125, 0.25, 0.625],
                [0.125, 0.125, 0.75],
            ],
            list(self.generate_values(3, 9, with_zero_values=False)),
        )
