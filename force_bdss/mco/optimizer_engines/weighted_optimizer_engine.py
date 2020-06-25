#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import logging
from functools import partial

import numpy as np

from traits.api import Enum, Str, Instance

from force_bdss.api import PositiveInt
from force_bdss.mco.optimizer_engines.space_sampling import (
    UniformSpaceSampler,
    DirichletSpaceSampler,
)
from force_bdss.mco.optimizers.i_optimizer import IOptimizer

from .base_optimizer_engine import BaseOptimizerEngine

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

        for _, optimal_kpis in weighted_optimize(weights):
            extrema[i] += np.asarray(optimal_kpis)

    scaling_factors = np.reciprocal(extrema.max(0) - extrema.min(0))
    return scaling_factors


class WeightedOptimizerEngine(BaseOptimizerEngine):
    """ A priori multi-objective optimization.

    Notes
    -----
    A multi-objective function is optimized by the a priori method of
    weighting/scalarisation. That is:
    1) Create a single objective from the weighted sum of the muLtiple
    objectives.
    2) The single-objective function is optimized.
    3) By sampling a range of weight combinations, part or all of the
    Pareto-efficient set is found.

    The weights are calculated by:
    1) For each objective calculate a "scale" by Sen's method: Optimize each
    objective individually to find both it's minimum and maximum. Use these
    to calculate its "scale".
    2) weight = scale x uniform-random-variate[0, 1), where
    SUM(variates) over objectives = 1.0
    """

    #: Optimizer name
    name = Str("Weighted_Optimizer")

    #: Search grid resolution per KPI
    num_points = PositiveInt(7)

    #: Method to calculate KPIs normalization coefficients
    scaling_method = Str("sen_scaling_method")

    #: Space search distribution for weight points sampling
    space_search_mode = Enum("Uniform", "Dirichlet")

    #: IOptimizer class that provides library backend for optimizing a
    #: callable
    optimizer = Instance(IOptimizer, transient=True)

    def optimize(self, **kwargs):
        """ Generates optimization results.

        Yields
        ----------
        optimization result: tuple(np.array, np.array, list)
            Point of evaluation, objective value, weights
        """

        #: Get non-zero weight combinations for each KPI
        scaling_factors = self.get_scaling_factors()

        #: loop through weight combinations
        for weights in self.weights_samples():
            log.info("Doing MCO run with weights: {}".format(weights))

            #: multiply weights by scales
            scaled_weights = [
                weight * scale
                for weight, scale in zip(weights, scaling_factors)
            ]

            #: optimize
            for point, kpis in self._weighted_optimize(
                    scaled_weights, **kwargs):
                yield point, kpis, scaled_weights

    def weights_samples(self, **kwargs):
        """ Generates necessary number of search space sample points
        from the `space_search_mode` search strategy."""
        return self._space_search_distribution(
            **kwargs
        ).generate_space_sample()

    def _weighted_optimize(self, weights, **kwargs):
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

        # Clear the KPI cache at the start of the optimization
        self._kpi_cache = {}

        log.info(
            "Running optimisation."
            + "Initial point: {}".format(self.initial_parameter_value)
            + "Bounds: {}".format(self.parameter_bounds)
        )

        # partial of objective function.
        weighted_score_func = partial(
            self._weighted_score, weights=weights)

        # optimize and evaluate
        for point in self.optimizer.optimize_function(
                weighted_score_func,
                self.parameters,
                **kwargs):

            # retrieve the function at the optimal point
            kpis = self.retrieve_result(point)

            log.info(
                "Optimal point : {}".format(point)
                + "KPIs at optimal point : {}".format(kpis)
            )

            yield point, kpis

    def _weighted_score(self, input_point, weights):
        """ Calculates the weighted score of the KPI vector at `input_point`,
        by taking dot product with a vector of `weights`."""

        # Calculate the value of the raw objective function
        score = self._score(input_point)

        # Return the score to be minimized
        score = np.dot(weights, score)
        log.info("Weighted score: {}".format(score))
        return score

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
