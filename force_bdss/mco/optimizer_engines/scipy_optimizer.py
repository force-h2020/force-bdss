import logging

from scipy import optimize as scipy_optimize

from traits.api import (
    Enum,
    provides,
    HasStrictTraits
)

from .i_optimizer import IOptimizer

log = logging.getLogger(__name__)


@provides(IOptimizer)
class ScipyOptimizer(HasStrictTraits):
    """ Performs local optimization of multiobjective function using scipy.
    The multiobjective function is converted to a scalar by dot product
    with a weights vector (`weighted_score`).
    """

    #: Algorithms available to work with
    algorithms = Enum("SLSQP", "Nelder-Mead", "Powell", "CG", "BFGS",
                      "Newton-CG", "L-BFGS-B", "TNC", "COBYLA",
                      "trust-constr", "dogleg",
                      "trust-ncg", "trust-exact", "trust-krylov")

    def optimize_function(self, func, x0, bounds):
        """ The core functionality offered by this class.
        Minimizes the function passed.
        """
        optimization_result = scipy_optimize.minimize(
            func,
            x0,
            method=self.algorithms,
            bounds=bounds,
        )
        optimal_point = optimization_result.x

        return optimal_point
