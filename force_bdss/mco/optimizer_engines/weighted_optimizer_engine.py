import logging
from functools import partial
import numpy as np

from traits.api import Enum, Str

from force_bdss.api import PositiveInt

from .scipy_optimizer_engine import ScipyOptimizerEngine

from force_bdss.mco.optimizer_engines.space_sampling import (
    UniformSpaceSampler,
    DirichletSpaceSampler,
)

log = logging.getLogger(__name__)


def sen_scaling_method(dimension, weighted_optimize):
    """ Calculate the default Sen's scaling factors for the
    "Multi-Objective Programming Method" [1].

    Parameters
    ----------
    dimension: int
        Number of KPIs, used in the optimization process

    weighted_optimize: unbound method
        Callable function with `weights` as the argument. Must return scalar
        objective value.

    Returns
    -------
    scaling_factors: np.array
        Sen's scaling factors

    References
    ----------
    [1] Chandra Sen, "Sen's Multi-Objective Programming Method and Its
       Comparison with Other Techniques", American Journal of Operational
       Research, vol. 8, pp. 10-13, 2018
    """
    extrema = np.zeros((dimension, dimension))

    initial_weights = np.eye(dimension)

    for i, weights in enumerate(initial_weights):

        log.info(f"Doing extrema MCO run with weights: {weights}")

        _, optimal_kpis = weighted_optimize(weights)
        extrema[i] += np.asarray(optimal_kpis)

    scaling_factors = np.reciprocal(extrema.max(0) - extrema.min(0))
    return scaling_factors


class WeightedOptimizerEngine(ScipyOptimizerEngine):
    """ Performs local optimization of multiobjective function using scipy.
    The multiobjective function is converted to a scalar by dot product
    with a weights vector (`weighted_score`).
    """

    #: Optimizer name
    name = Str("Weighted_Optimizer")

    #: Search grid resolution per KPI
    num_points = PositiveInt(7)

    #: Method to calculate KPIs normalization coefficients
    scaling_method = Str("sen_scaling_method")

    #: Space search distribution for weight points sampling
    space_search_mode = Enum("Uniform", "Dirichlet")

    def weighted_score(self, input_point, weights):
        """ Calculates the weighted score of the KPI vector at `input_point`,
        by taking dot product with a vector of `weights`."""
        score = np.dot(weights, self._score(input_point))
        log.info("Weighted score: {}".format(score))
        return score

    def optimize(self):
        """ Generates optimization results with weighted optimization.

        Yields
        ----------
        optimization result: tuple(np.array, np.array, list)
            Point of evaluation, objective value, dummy list of weights
        """
        #: Get scaling factors and non-zero weight combinations for each KPI
        scaling_factors = self.get_scaling_factors()
        for weights in self.weights_samples():
            log.info("Doing MCO run with weights: {}".format(weights))

            scaled_weights = [
                weight * scale
                for weight, scale in zip(weights, scaling_factors)
            ]

            optimal_point, optimal_kpis = self._weighted_optimize(
                scaled_weights
            )
            yield optimal_point, optimal_kpis, scaled_weights

    def _weighted_optimize(self, weights):
        """ Performs single scipy.minimize operation on the dot product of
        the multiobjective function with `weights`.

        Parameters
        ----------
        weights: List[Float]
            Weights for each KPI objective

        Returns
        ----------
        optimization result: tuple(np.array, np.array)
            Point of evaluation, and objective values
        """
        log.info(
            "Running optimisation."
            + "Initial point: {}".format(self.initial_parameter_value)
            + "Bounds: {}".format(self.parameter_bounds)
        )

        weighted_score_func = partial(self.weighted_score, weights=weights)

        return self._scipy_optimize(weighted_score_func)

    def get_scaling_factors(self):
        """ Calculates scaling factors for KPIs, defined in MCO.
        Scaling factors are calculated (as required) by the provided scaling
        method. In general, this provides normalization values for the possible
        range of each KPI.
        Performs scaling for all KPIs that have `auto_scale == True`.
        Otherwise, keeps the default `scale_factor`.
        """
        if self.scaling_method == "sen_scaling_method":
            scaling_method = sen_scaling_method
        else:
            raise NotImplementedError(
                f"Scaling method with name {self.scaling_method} is not found."
            )

        #: Get default scaling weights for each KPI variable
        default_scaling_factors = np.array(
            [kpi.scale_factor for kpi in self.kpis]
        )

        #: Apply a wrapper for the evaluator weights assignment and
        #: call of the .optimize method.
        #: Then, calculate scaling factors defined by the `scaling_method`
        scaling_factors = scaling_method(
            len(self.kpis), self._weighted_optimize
        )

        #: Apply the scaling factors where necessary
        auto_scales = [kpi.auto_scale for kpi in self.kpis]
        default_scaling_factors[auto_scales] = scaling_factors[auto_scales]

        log.info(
            "Using KPI scaling factors: {}".format(default_scaling_factors)
        )

        return default_scaling_factors.tolist()

    def _space_search_distribution(self, **kwargs):
        """ Creates a space search distribution object, based on
        the user settings of the `space_search_mode` attribute."""

        if self.space_search_mode == "Uniform":
            distribution = UniformSpaceSampler
        elif self.space_search_mode == "Dirichlet":
            distribution = DirichletSpaceSampler
        else:
            raise NotImplementedError
        return distribution(len(self.kpis), self.num_points, **kwargs)

    def weights_samples(self, **kwargs):
        """ Generates necessary number of search space sample points
        from the `space_search_mode` search strategy."""
        return self._space_search_distribution(
            **kwargs
        ).generate_space_sample()
