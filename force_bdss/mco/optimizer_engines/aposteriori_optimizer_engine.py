import logging
import abc

from traits.api import Str, Property

from .base_optimizer_engine import BaseOptimizerEngine

log = logging.getLogger(__name__)


class AposterioriOptimizerEngine(BaseOptimizerEngine):
    """ A posteriori multi-objective optimization.

    Notes
    -----
    A multi-objective function is optimized using the a posteriori
    method of a multi-objective optimizer (e.g. Nevergrad).
    The optimization result is some part of the Pareto-efficient set.
    """

    #: Optimizer name
    name = Str("APosteriori_Optimizer")

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

    def optimize(self, *vargs):
        """ Generates optimization results.

        Yields
        ----------
        optimization result: tuple(np.array, np.array, list)
            Point of evaluation, objective value
        """
        #: get pareto set
        pareto = self.optimize_function(
            self._score,
            self.initial_parameter_value,
            self.parameter_bounds
        )
        for optimal_point in pareto:
            optimal_kpis = self._score(optimal_point)
            yield optimal_point, optimal_kpis

    def unpacked_score(self, *unpacked_input):
        packed_input = list(unpacked_input)
        return self._score(packed_input)

    @abc.abstractmethod
    def optimize_function(self, func, x0, bounds):
        """ A wrapper for the optimizer. Any subclass of this class
        can implement this function by also inheriting a mixin class
        implementing the IOptimizer interface.
        """
