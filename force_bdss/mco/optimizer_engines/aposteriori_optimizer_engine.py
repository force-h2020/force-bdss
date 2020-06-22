#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import logging

from traits.api import Str, Instance

from force_bdss.mco.optimizers.i_optimizer import IOptimizer

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

    #: IOptimizer class that provides library backend for optimizing a
    #: callable
    optimizer = Instance(IOptimizer, transient=True)

    def optimize(self, **kwargs):
        """ Generates optimization results.

        Yields
        ----------
        optimization result: tuple(array-like, array-like)
            MCO parameter and KPI values at point of optimization
        """
        self._kpi_cache = {}

        #: get pareto set
        for point in self.optimizer.optimize_function(
                self._score,
                self.parameters,
                **kwargs):
            # Retrieve the cached raw KPI values
            kpis = self._kpi_cache[tuple(point)]
            yield point, kpis

    def unpacked_score(self, *unpacked_input):
        packed_input = list(unpacked_input)
        return self._score(packed_input)
