import abc
import logging

from traits.api import Interface

log = logging.getLogger(__name__)


class IOptimizer(Interface):
    """ The optimizer used by an optimizer engine.

    Extended Summary
    ----------------
    An implementing class will be specific to an optimizer library. e.g.

    @provides(IOptimizer)
    class ScipyOptimizer():

    Any subclass of BaseOptimizerEngine can inherit such a class
    and then call optimize_function() within its optimize().
    """
    @abc.abstractmethod
    def optimize_function(self, func, x0, bounds):
        """ Optimize a function, according to the library (scipy/etc).

        Parameters
        ----------
        func: Callable
            The function to be optimized.
        x0: np.array
            initial point
        bounds: tuple
            parameter bounds
        Return
        ------
        Tuple
            optimal_point
        """
