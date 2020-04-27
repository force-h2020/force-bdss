import abc
import logging

from traits.api import Interface

log = logging.getLogger(__name__)


class IOptimizer(Interface):
    """ The optimizer used by an optimizer engine.
    """
    @abc.abstractmethod
    def optimize_function(self, func, x0, bounds):
        """ Optimize a function, according to the library (scipy/etc).
        """
