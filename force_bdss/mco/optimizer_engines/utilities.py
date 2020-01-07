import abc
import numpy as np

from traits.api import ABCHasStrictTraits, Bool, ListFloat
from force_bdss.api import PositiveInt


def convert_by_mask(array, kpi_mask, key="MINIMISE"):
    """ Given the `array` of (KPI) values, changes the sign of the
    `array` entries if the corresponding `kpi_mask` entry is different
    from the `key`.
    Example:
        If the `key` is 'MINIMISE', and `kpi_mask[i]` value is 'MINIMISE',
        we don't change the sign of the array entry `array[i]`.
        Otherwise, we do change the sign.

    Parameters
    ----------
    array: List[int, float], np.array
        array of (KPI) values to change sign of
    kpi_mask: List[_type], np.array
        mask array to compare with key value
    key: object(_type)
        reference comparison value

    Returns
    --------
    substituted_values: np.array
        New array with the elements corresponding to kpi_mask == key
        are inverted by _a -> -_a
    """
    np_kpi_mask = np.array(kpi_mask)
    np_array = np.array(array)
    return np.where(np_kpi_mask == key, np_array, -np_array)


def resolution_to_sample_size(space_dimension, n_points):
    """ Calculates what is the exact number of space samples (vectors
    of dimension `space_dimension`) we should pick, in order to have
    an effective sampling resolution of `nof_points` per dimension.
    This method unifies the number of samples from stochastic space
    search models and the number of samples from the uniform-along-each-axis
    sampling.
    """
    samples_total = (
        np.math.factorial(space_dimension + n_points - 2)
        / np.math.factorial(space_dimension - 1)
        / np.math.factorial(n_points - 1)
    )
    return int(samples_total)


class SpaceSampler(ABCHasStrictTraits):
    """ Base class for search space sampling from various distributions.

    Given the dimension of the sample vectors and the sampling resolution
    along each of the dimensions, SpaceSampler can generate sampling points
    with `generate_space_sample`.
    The space search satisfies the requirement that the l1-norm of all sample
    points always equals 1.0.
    """

    #: the dimension of the sample vectors
    dimension = PositiveInt()

    #: the number of (effective) divisions along each dimension
    resolution = PositiveInt()

    def __init__(self, dimension, resolution, **kwargs):
        super().__init__(dimension=dimension, resolution=resolution, **kwargs)

    @abc.abstractmethod
    def _get_sample_point(self):
        """ Internal generator of sample points from the distribution.
        Returns or yields a sampled point.
        """

    @abc.abstractmethod
    def generate_space_sample(self, *args, **kwargs):
        """ Generates search space samples. The number of returned points
        is calculated here, if `_get_sample_point` method is a random
        sampler.

        Yields
        -------
        generator
            random samples of vector satisfying the sum(p) = 1 and
            distribution constraints
        """


class DirichletSpaceSampler(SpaceSampler):
    """ Search space sampler class with probability distribution function
    defined by the Dirichlet distribution [1].

    The distribution is "fair": it provides equal probability for each
    component of the sample vector. The user can control the distribution shape
    by changing `alpha`:
    - Samples are closer to bounds for alpha < 1,
    - Samples are concentrated in the middle of the
    search space for alpha > 1,
    - All samples have equal probability for alpha = 1

    A nice visualization of the Dirichlet distribution can be found at [2].

    References
    -------
    [1] https://en.wikipedia.org/wiki/Dirichlet_distribution
    [2] http://blog.bogatron.net/blog/2014/02/02/visualizing-dirichlet-\
    distributions/
    """

    #: Dirichlet distribution parameter
    alpha = ListFloat()

    #: Distribution generation function
    _distribution_function = np.random.dirichlet

    def __init__(self, dimension, resolution, alpha=None, **kwargs):
        super().__init__(dimension, resolution, **kwargs)

        if alpha is None:
            _centering_coef = 1.0
        else:
            _centering_coef = alpha

        self.alpha = [_centering_coef] * self.dimension

    def _get_sample_point(self):
        return self._distribution_function(self.alpha).tolist()

    def generate_space_sample(self):
        n_points = resolution_to_sample_size(self.dimension, self.resolution)
        for _ in range(n_points):
            yield self._get_sample_point()


class UniformSpaceSampler(SpaceSampler):
    """ UniformSpaceSampler provides all possible combinations of weights
    adding to 1, such that the sampling points are uniformly distributed along
    each axis. For example, a dimension 3 will give all combinations (x, y, z),
    where
    $ x + y + z = 1.0,
    and (x, y, z) can realise only specified equidistant values.

    The `resolution` parameter indicates how many divisions along a single
    dimension will be performed. For example `resolution = 3` will evaluate
    for x being 0.0, 0.5 and 1.0.

    Parameter `with_zero_values` controls the presence of zero valued entries.
    If `with_zero_values` parameter is set to False, then ensure
    `resolution > dimension` in order for the generator to return any values.
    """

    #: Controls whether zero entries can appear in sample vector
    with_zero_values = Bool(False)

    def generate_space_sample(self, **kwargs):
        yield from self._get_sample_point()

    def _get_sample_point(self):
        """
        Yields
        ----------
            Yields all the possible combinations satisfying the requirement
            that the sum of all the weights must always be 1.0
        """

        scaling = 1.0 / (self.resolution - 1)
        for int_w in self._int_weights():
            yield [scaling * val for val in int_w]

    def _int_weights(self, resolution=None, dimension=None):
        """Helper routine for the `_get_sample_point`. Generates integer values
        vectors, whose l1-norm equal `resolution`."""

        if dimension is None:
            dimension = self.dimension

        if resolution is None:
            resolution = self.resolution

        if dimension == 1:
            yield [resolution - 1]
        else:
            if self.with_zero_values:
                integers = np.arange(resolution - 1, -1, -1)
            else:
                integers = np.arange(resolution - 2, 0, -1)
            for i in integers:
                for entry in self._int_weights(resolution - i, dimension - 1):
                    yield [i] + entry
