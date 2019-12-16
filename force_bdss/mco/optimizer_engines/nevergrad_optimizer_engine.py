import logging
import numpy as np
import nevergrad as ng
from nevergrad.functions import MultiobjectiveFunction

from traits.api import Enum, Unicode, Property

from force_bdss.api import PositiveInt
from .base_optimizer_engine import BaseOptimizerEngine

log = logging.getLogger(__name__)


class NevergradTypeError(Exception):
    pass


class NevergradOptimizerEngine(BaseOptimizerEngine):

    #: Optimizer name
    name = Unicode("Nevergrad")

    #: Algorithms available to work with
    algorithms = Enum(*ng.optimizers.registry.keys())

    #: Optimization budget defines the allowed number of objective calls
    budget = PositiveInt(500)

    kpi_bounds = Property(depends_on="kpis.[scale_factor]")

    def _algorithms_default(self):
        return "TwoPointsDE"

    def _create_instrumentation_variable(self, parameter):
        """ Create nevergrad.variable from `MCOParameter`. Different
        MCOParameter subclasses have different signature attributes.
        The mapping between MCOParameters and nevergrad types is bijective.

        Parameters
        ----------
        parameter: BaseMCOParameter
            object to convert to nevergrad type

        Returns
        ----------
        nevergrad_parameter: nevergrad.Variable
            nevergrad variable of corresponding type
        """
        if hasattr(parameter, "lower_bound") and hasattr(
            parameter, "upper_bound"
        ):
            # The affine transformation with `slope` before `bounded` cab be
            # used to normalize the distribution of points in internal space.
            # This allows better exploration of the boundary regions. This
            # feature is still in research mode, and presumably must be for
            # the user to play with. Implementation would be:
            # >>> affine_slope = 1.0
            # >>> var = ng.var.Scalar().affined(affine_slope, 0).bounded(...)
            return ng.var.Scalar().bounded(
                parameter.lower_bound, parameter.upper_bound
            )
        elif hasattr(parameter, "value"):
            return ng.var._Constant(value=parameter.value)
        elif hasattr(parameter, "levels"):
            return ng.var.OrderedDiscrete(parameter.sample_values)
        elif hasattr(parameter, "categories"):
            return ng.var.SoftmaxCategorical(
                possibilities=parameter.sample_values, deterministic=True
            )
        else:
            raise NevergradTypeError(
                f"Can not convert {parameter} to any of"
                " supported Nevergrad types"
            )

    def _assemble_instrumentation(self, parameters=None):
        """ Assemble nevergrad.Instrumentation object from `parameters` list.

        Parameters
        ----------
        parameters: List(BaseMCOParameter)
            parameter objects containing lower and upper numerical bounds

        Returns
        ----------
        instrumentation: ng.Instrumentation
        """
        if parameters is None:
            parameters = self.parameters

        instrumentation = [
            self._create_instrumentation_variable(p) for p in parameters
        ]
        return ng.Instrumentation(*instrumentation)

    def _get_kpi_bounds(self):
        """ Assemble optimization bounds on KPIs, provided by
        the `scale_factor` attributes.
        Note: Ideally, an `upper_bound` kpi attribute should be
        responsible for the bounds.

        Parameters
        ----------
        kpis: List(KPISpecification)
            kpi objects containing upper numerical bounds

        Returns
        ----------
        upper_bounds: np.array
            kpis upper bounds
        """
        upper_bounds = np.zeros(len(self.kpis))
        for i, kpi in enumerate(self.kpis):
            try:
                upper_bounds[i] = kpi.scale_factor
            except AttributeError:
                upper_bounds[i] = 100
        return upper_bounds

    def optimize(self):
        """ Constructs objects required by the nevergrad engine to
        perform optimization.

        Yields
        ----------
        optimization result: tuple(np.array, np.array, list)
            Point of evaluation, objective value, dummy list of weights
        """
        f = MultiobjectiveFunction(
            multiobjective_function=self._score, upper_bounds=self.kpi_bounds
        )
        instrumentation = self._assemble_instrumentation()
        instrumentation.random_state.seed(12)
        ng_optimizer = ng.optimizers.registry[self.algorithms](
            instrumentation=instrumentation, budget=self.budget
        )
        for _ in range(ng_optimizer.budget):
            x = ng_optimizer.ask()
            value = f.multiobjective_function(x.args)
            volume = f.compute_aggregate_loss(
                self._minimization_score(value), *x.args, **x.kwargs
            )
            ng_optimizer.tell(x, volume)

            if self.verbose_run:
                yield x.args, value, [1] * len(self.kpis)

        if not self.verbose_run:
            for point, value in f._points:
                value = self._minimization_score(value)
                yield point[0], value, [1] * len(self.kpis)
