from unittest.case import TestCase

import numpy as np

from force_bdss.mco.optimizer_engines.space_sampling import (
    UniformSpaceSampler, DirichletSpaceSampler,
    SpaceSampler, resolution_to_sample_size)


class TestSpaceSampling(TestCase):

    def test_resolution_to_sample_size(self):

        self.assertEqual(1, resolution_to_sample_size(1, 1))
        self.assertEqual(1, resolution_to_sample_size(1, 10))
        self.assertEqual(1, resolution_to_sample_size(3, 1))
        self.assertEqual(6, resolution_to_sample_size(3, 3))
        self.assertEqual(715, resolution_to_sample_size(5, 10))


class BaseTestSampler(TestCase):

    distribution = SpaceSampler

    def setUp(self):
        self.dimensions = [1, 3, 5]
        self.resolutions = [1, 3, 10]

    def assertArrayAlmostEqual(self, array_like1, array_like2):
        return self.assertTrue(
            np.allclose(array_like1, array_like2))

    def generate_values(self, *args, **kwargs):
        return self.distribution(*args, **kwargs).generate_space_sample(
            **kwargs
        )

    def generate_samplers(self, **kwargs):
        for dimension in self.dimensions:
            for resolutions in self.resolutions:
                yield self.distribution(
                    dimension, resolutions, **kwargs
                )

    def generate_space_samples(self, **kwargs):
        for sampler in self.generate_samplers(**kwargs):
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

    def generate_weights(self, *args, **kwargs):
        return self.distribution(*args, **kwargs)._int_weights()

    def test__int_weights(self):

        self.assertListEqual(
            [[1]],
            list(self.generate_weights(1, 1))
        )
        self.assertListEqual(
            [[0]],
            list(self.generate_weights(1, 1, with_zero_values=True))
        )

        self.assertListEqual(
            [[1, 1]],
            list(self.generate_weights(2, 1))
        )
        self.assertListEqual(
            [[0, 0]],
            list(self.generate_weights(2, 1, with_zero_values=True))
        )

        self.assertListEqual(
            [[3, 1], [2, 2], [1, 3]],
            list(self.generate_weights(2, 3))
        )
        self.assertListEqual(
            [[2, 0], [1, 1], [0, 2]],
            list(self.generate_weights(2, 3, with_zero_values=True))
        )

    def test_space_sample_values(self):

        self.assertArrayAlmostEqual(
            [[5/6, 1/6], [2/3, 1/3], [0.5, 0.5], [1/3, 2/3], [1/6, 5/6]],
            list(self.generate_values(2, 5,)),
        )
        self.assertEqual(
            [[1.0, 0.0], [0.75, 0.25], [0.50, 0.50], [0.25, 0.75], [0.0, 1.0]],
            list(self.generate_values(2, 5, with_zero_values=True)),
        )

    def test_generate_space_sample(self):
        for with_zero_values in [False, True]:
            self.generate_space_samples(
                with_zero_values=with_zero_values)


class TestDirichletSpaceSampler(BaseTestSampler):

    distribution = DirichletSpaceSampler

    def setUp(self):
        super().setUp()
        self.alphas = [1, 0.5, 10]

    def test__get_sample_point(self):
        for alpha in self.alphas:
            for sampler in self.generate_samplers(alpha=alpha):
                self.assertAlmostEqual(
                    1.0, sum(sampler._get_sample_point()))

    def test_generate_space_sample(self):
        for alpha in self.alphas:
            self.generate_space_samples(alpha=alpha)
