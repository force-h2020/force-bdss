import abc
import logging
import numpy as np

from traits.api import ABCHasStrictTraits, List, Instance, Bool

from force_bdss.api import KPISpecification, BaseMCOParameter, IEvaluator
from force_bdss.io.workflow_writer import pop_dunder_recursive

log = logging.getLogger(__name__)


class BaseOptimizerEngine(ABCHasStrictTraits):
    """
    Optimizer Engine performs black-box optimization (minimization) of
    the KPI values by exploring the space of input parameters. The way
    the input space is explored is subject to the developer to implement.
    Users should be able to choose an Optimizer Engine, setup the optimization
    parameters, and get optimized data from the OptimizerEngine.optimize
    method.
    """

    #: A list of the input parameters representing the search space
    parameters = List(BaseMCOParameter, visible=False, transient=True)

    #: A list of the output KPI parameters representing
    #: the optimization objective(s)
    kpis = List(KPISpecification, visible=False, transient=True)

    #: Executes the workflow with given input parameters and returns
    #: the KPIs of the workflow
    #: Note: rename to `evaluator`. This will break existing API
    single_point_evaluator = Instance(
        IEvaluator, visible=False, transient=True
    )

    #: Yield data points on each workflow evaluation
    verbose_run = Bool(False)

    @abc.abstractmethod
    def optimize(self):
        """ Main entry point to the OptimizerEngine. This is an general
        iterator over [explored input space, objective space, **kwargs].
        It can yield data as a single workflow evaluation has been completed,
        or return the optimization data after all required computations
        have finished.
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


def convert_by_mask(array, kpi_mask, key="MINIMISE"):
    """ Given the `array` of (KPI) values, changes the sign of the
    `array` entries if the corresponding `kpi_mask` entry is different
    from the `key`.
    Example:
        If the `key` is 'MINIMISE', and `kpi_mask[i]` value is 'MINIMISE',
        we don't change the sign of the array entry `array[i]`.
        Otherwise, we do change the sign.

    Parameters
    ----------
    array: List[int, float], np.array
        array of (KPI) values to change sign of
    kpi_mask: List[_type], np.array
        mask array to compare with key value
    key: object(_type)
        reference comparison value

    Returns
    --------
    substituted_values: np.array
        New array with the elements corresponding to kpi_mask == key
        are inverted by _a -> -_a
    """
    np_kpi_mask = np.array(kpi_mask)
    np_array = np.array(array)
    return np.where(np_kpi_mask == key, np_array, -np_array)
