#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import abc
import logging

from traits.api import (
    ABCHasStrictTraits, List, Instance, Bool, Property, Dict)

from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.i_evaluator import IEvaluator
from force_bdss.mco.optimizer_engines.utilities import convert_to_score
from force_bdss.utilities import pop_dunder_recursive

log = logging.getLogger(__name__)


class BaseOptimizerEngine(ABCHasStrictTraits):
    """
    Optimizer Engine performs black-box optimization (minimization) of
    the KPI values by exploring the space of input parameters. Developer
    implements the input space search strategy, and how the minimization
    is performed.
    Users should be able to choose an Optimizer Engine, setup the optimization
    parameters, and get optimized data from the OptimizerEngine.optimize
    method.
    """

    #: A list of the input parameters representing the search space
    parameters = List(BaseMCOParameter, visible=False, transient=True)

    #: A list of the output KPI parameters representing the objective(s)
    kpis = List(KPISpecification, visible=False, transient=True)

    #: Object that Executes the workflow with given input parameters
    #: and returns the KPI values of the workflow.
    #: Note: rename to `evaluator`. This will break existing API
    single_point_evaluator = Instance(
        IEvaluator, visible=False, transient=True
    )

    #: Caches KPI values between optimization runs
    _kpi_cache = Dict(transient=True)

    #: Default (initial) guess on input parameter values
    initial_parameter_value = Property(
        depends_on="parameters.[initial_value]", visible=False
    )

    #: Input parameter bounds. Defines the search space.
    parameter_bounds = Property(
        depends_on="parameters.[lower_bound, upper_bound]", visible=False
    )

    #: Input parameter bounds. Defines the search space.
    kpi_bounds = Property(
        depends_on="kpis.[lower_bound, upper_bound]", visible=False
    )

    #: Yield data points on each workflow evaluation, or return filtered
    #: data, e.g. Pareto front only
    verbose_run = Bool(False)

    def _get_initial_parameter_value(self):
        return [p.initial_value for p in self.parameters]

    def _get_parameter_bounds(self):
        return [(p.lower_bound, p.upper_bound) for p in self.parameters]

    def _get_kpi_bounds(self):
        return [(kpi.lower_bound, kpi.upper_bound) for kpi in self.kpis]

    @abc.abstractmethod
    def optimize(self, **kwargs):
        """ Main entry point to the OptimizerEngine. This is a general
        iterator, expected to yield both optimal values of MCO parameters
        and the corresponding KPIs. Additional values can also be returned,
        though they will need to be handled by any implementation calling
        the method.

        Any data points yielded will be communicated with the rest of the BDSS
        framework as soon as they are generated, so a long optimization
        procedure may wish to periodically report optimal values, rather than
        returning all points at the end of the MCO. It is also expected that
        the `verbose_run` attribute may be used to control the number of
        data points reported.

        Although this method expects no arguments, it may be passed in
        additional keywords if required. This can be useful when using
        an `IOptimizer` class to provide a wrapper around an optimization
        library.
        """

    def _score(self, input_point):
        """ Evaluates the workflow state at the `input_point` using the
        `single_point_evaluator`, and returns the resulting KPI data.
        This method abstracts away the `single_point_evaluator` call
        from the rest of the OptimizerEngine methods and the user.
        This is also useful for the testing purposes, when the `evaluate`
        method is mocked.
        """

        # Calculate and cache the raw KPI values
        kpi_values = self.single_point_evaluator.evaluate(input_point)
        self._kpi_cache[tuple(input_point)] = kpi_values

        # Return the score to be minimized
        score = self._minimization_score(kpi_values)
        log.info("Objective score: {}".format(score))
        return score

    def _minimization_score(self, score):
        """ Transforms the optimization `score` array to the minimization
        format. The minimization format implies that all optimization KPIs
        are subject to minimization."""
        return convert_to_score(score, self.kpis)

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())
