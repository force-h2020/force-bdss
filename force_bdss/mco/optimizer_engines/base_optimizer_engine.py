import abc
import logging

from traits.api import ABCHasStrictTraits, List, Instance, Bool

from force_bdss.core.kpi_specification import KPISpecification
from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.i_evaluator import IEvaluator
from force_bdss.io.workflow_writer import pop_dunder_recursive
from force_bdss.mco.optimizer_engines.utilities import convert_by_mask

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

    #: Yield data points on each workflow evaluation, or return filtered
    #: data, e.g. Pareto front only
    verbose_run = Bool(False)

    @abc.abstractmethod
    def optimize(self):
        """ Main entry point to the OptimizerEngine. This is a general
        iterator. It yields [explored input space, objective space, kwargs].
        It can yield data as a single workflow evaluation has been completed
        (if `verbose_run` is True), or return the optimization data after all
        required computations have finished (if `verbose_run` is False).
        """

    def _score(self, input_point):
        """ Evaluates the workflow state at the `input_point` using the
        `single_point_evaluator`, and returns the resulting KPI data.
        This method abstracts away the `single_point_evaluator` call
        from the rest of the OptimizerEngine methods and the user.
        This is also useful for the testing purposes, when the `evaluate`
        method is mocked.
        """
        score = self.single_point_evaluator.evaluate(input_point)
        log.info("Objective score: {}".format(score))
        return score

    def _minimization_score(self, score):
        """ Transforms the optimization `score` array to the minimization
        format. The minimization format implies that all optimization KPIs
        are subject to minimization."""
        return convert_by_mask(
            score, [kpi.objective for kpi in self.kpis], "MINIMISE"
        )

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())