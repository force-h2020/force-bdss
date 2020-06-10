#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import logging

from traits.api import Str, Instance, Enum, Int

from force_bdss.mco.optimizers.i_optimizer import IOptimizer

from .base_optimizer_engine import BaseOptimizerEngine

log = logging.getLogger(__name__)


class MonteCarloEngine(BaseOptimizerEngine):

    #: Optimizer name
    name = Str("Monte Carlo")

    # sample or optimize
    method = Enum(['sample', 'optimize'])

    # number of samples.
    n_sample = Int(100)

    #: IOptimizer class that provides library backend for optimizing a
    #: callable
    optimizer = Instance(IOptimizer, transient=True)

    def optimize(self, *vargs):
        """ Generates sampling/optimization results.

        Yields
        ----------
        optimization result: tuple(np.array, np.array, list)
            Point of evaluation, objective value
        """



        #: get pareto set
        for point in self.optimizer.optimize_function(
                self._score,
                self.parameters):
            kpis = self._score(point)
            yield point, kpis
