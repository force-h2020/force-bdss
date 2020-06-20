#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import abc
import logging

from traits.api import Interface

log = logging.getLogger(__name__)


class IOptimizer(Interface):
    """ The optimizer used by an optimizer engine.
    """

    @abc.abstractmethod
    def optimize_function(self, func, params, **kwargs):
        """ Optimizes a function, according to a specific library (scipy/etc).

        Parameters
        ----------
        func: Callable
            The "objective" function to optimize. Must have the
            signature: func(<list of BaseMCOParameter values>)
        params: list of BaseMCOParameter objects
            The BaseMCOParameter objects corresponding to the values.

        Yields
        ------
        list of BaseMCOParameter values
            The optimal set of parameters (point in parameter space).
        """
