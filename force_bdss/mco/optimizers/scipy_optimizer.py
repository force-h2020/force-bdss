from traits.api import (
    Enum,
    provides,
    HasStrictTraits
)

from force_bdss.mco.optimizers.i_optimizer import IOptimizer

from scipy import optimize as scipy_optimize


@provides(IOptimizer)
class ScipyOptimizer(HasStrictTraits):
    """ Optimization of a scalar function using scipy.
    """

    #: Algorithms available to work with
    algorithms = Enum("SLSQP", "Nelder-Mead", "Powell", "CG", "BFGS",
                      "Newton-CG", "L-BFGS-B", "TNC", "COBYLA",
                      "trust-constr", "dogleg",
                      "trust-ncg", "trust-exact", "trust-krylov")

    def optimize_function(self, func, x0, bounds):
        """ Minimize the passed function.
        """
        optimization_result = scipy_optimize.minimize(
            func,
            x0,
            method=self.algorithms,
            bounds=bounds,
        )
        optimal_point = optimization_result.x

        return optimal_point
