from unittest.case import TestCase

import numpy as np

from force_bdss.mco.optimizer_engines.space_sampling import (
    UniformSpaceSampler, DirichletSpaceSampler,
    SpaceSampler)


class BaseTestSampler(TestCase):
    distribution = SpaceSampler

    def generate_values(self, *args, **kwargs):
        return self.distribution(*args, **kwargs).generate_space_sample(
            **kwargs
        )

    def assertArrayAlmostEqual(self, array_like1, array_like2):
        return self.assertTrue(
            np.allclose(array_like1, array_like2))


class TestUniformSpaceSampler(BaseTestSampler):
    distribution = UniformSpaceSampler

    def generate_weights(self, *args, **kwargs):
        return self.distribution(*args, **kwargs)._int_weights()

    def test__int_weights(self):

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

    def test_space_sample(self):

        self.assertEqual(
            [[1.0]],
            list(self.generate_values(1, 5))
        )
        self.assertEqual(
            [[1.0]],
            list(self.generate_values(1, 5, with_zero_values=True))
        )

        self.assertArrayAlmostEqual(
            [[5/6, 1/6], [2/3, 1/3], [0.5, 0.5], [1/3, 2/3], [1/6, 5/6]],
            list(self.generate_values(2, 5,)),
        )
        self.assertEqual(
            [[1.0, 0.0], [0.75, 0.25], [0.50, 0.50], [0.25, 0.75], [0.0, 1.0]],
            list(self.generate_values(2, 5, with_zero_values=True)),
        )

        # Assert all weights are normalised to 1
        for weights in self.generate_values(3, 10):
            self.assertAlmostEqual(1.0, sum(weights))
        for weights in self.generate_values(3, 10, with_zero_values=True):
            self.assertAlmostEqual(1.0, sum(weights))


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
                sampler.resolution
            )

            for sample in space_sample:
                self.assertAlmostEqual(1.0, sum(sample))
