import logging
import numpy as np

from scipy import optimize as scipy_optimize

from traits.api import Enum, Str, Property

from force_bdss.api import PositiveInt
from .base_optimizer_engine import BaseOptimizerEngine

log = logging.getLogger(__name__)


class ScipyOptimizerEngine(BaseOptimizerEngine):
    """ Performs local optimization of multiobjective function using scipy.
    The multiobjective function is converted to a scalar by dot product
    with a weights vector (`weighted_score`).
    """

    #: Optimizer name
    name = Str("Scipy_Optimizer")

    #: Algorithms available to work with
    algorithms = Enum("SLSQP", "Nelder-Mead", "Powell", "CG", "BFGS",
                      "Newton-CG", "L-BFGS-B", "TNC", "COBYLA",
                      "trust-constr", "dogleg",
                      "trust-ncg", "trust-exact", "trust-krylov")

    #: Default (initial) guess on input parameter values
    initial_parameter_value = Property(
        depends_on="parameters.[initial_value]", visible=False
    )

    #: Input parameter bounds. Defines the search space.
    parameter_bounds = Property(
        depends_on="parameters.[lower_bound, upper_bound]", visible=False
    )

    def _get_initial_parameter_value(self):
        return [p.initial_value for p in self.parameters]

    def _get_parameter_bounds(self):
        return [(p.lower_bound, p.upper_bound) for p in self.parameters]

    def optimize(self):
        """ Generates optimization results with weighted optimization.

        Yields
        ----------
        optimization result: tuple(np.array, np.array, list)
            Point of evaluation, objective value, dummy list of weights
        """
        optimal_point, optimal_kpis = self._scipy_optimize(
            self._scalar_score
        )
        yield optimal_point, optimal_kpis, []

    def _scalar_score(self, input_point):
        """ The sum of the objectives/kpis, so they can be
        optimized by scipy.
        """
        return np.sum(self._minimization_score(self._score(input_point)))

    def _scipy_optimize(self, func):
        """ The core functionality offered by this class.
        Minimizes the function passed.

        Parameters
        ----------
        func: Callable
            The function to be minimized by scipy.In the optimize()
            here this is just _score(). In a weighted subclass
            this is a partial of _score() with weights given.

        Returns
        -------
        optimization result: tuple(np.array, np.array)
            Point of evaluation, and objective values
        """

        optimization_result = scipy_optimize.minimize(
            func,
            self.initial_parameter_value,
            method=self.algorithms,
            bounds=self.parameter_bounds,
        )
        optimal_point = optimization_result.x
        optimal_kpis = self._score(optimal_point)

        log.info(
            "Optimal point : {}".format(optimal_point)
            + "KPIs at optimal point : {}".format(optimal_kpis)
        )

        return optimal_point, optimal_kpis
