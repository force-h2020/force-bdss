import logging
import numpy as np

from traits.api import Enum, Unicode, Function

from force_bdss.api import PositiveInt
from .base_optimizer_engine import BaseOptimizerEngine

log = logging.getLogger(__name__)


def sen_scaling_method(dimension, weighted_optimize):
    """ Calculate the default Sen's scaling factors for the
    "Multi-Objective Programming Method" [1].

    References
    ----------
    .. [1] Chandra Sen, "Sen's Multi-Objective Programming Method and Its
       Comparison with Other Techniques", American Journal of Operational
       Research, vol. 8, pp. 10-13, 2018

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
    """
    extrema = np.zeros((dimension, dimension))

    initial_weights = np.eye(dimension)

    for i, weights in enumerate(initial_weights):

        log.info(f"Doing extrema MCO run with weights: {weights}")

        _, optimal_kpis = weighted_optimize(weights)
        extrema[i] += np.asarray(optimal_kpis)

    scaling_factors = np.reciprocal(extrema.max(0) - extrema.min(0))
    return scaling_factors


class WeightedOptimizer(BaseOptimizerEngine):
    """Performs local optimization of multiobjective function
    using scipy. The multiobjective function is converted to a
    scalar by dot product with a weights vector.
    """

    #: Optimizer name
    name = Unicode("Weighted_Optimizer")

    #: Search grid resolution per KPI
    num_points = PositiveInt(7)

    #: Algorithms available to work with
    algorithms = Enum("SLSQP", "TNC")

    #: Method to calculate KPIs normalization coefficients
    scaling_method = Function(default_value=sen_scaling_method)

    def _score(self, input_point, weights):
        score = np.dot(weights, super()._score(input_point))
        log.info("Weighted score: {}".format(score))
        return score

    def optimize(self):
        pass
