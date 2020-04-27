from traits.api import (
    Enum,
    provides,
    HasStrictTraits
)
from force_bdss.api import PositiveInt

from force_bdss.mco.optimizers.i_optimizer import IOptimizer

import nevergrad as ng
from nevergrad.parametrization import core as ng_core
from nevergrad.functions import MultiobjectiveFunction

import logging
log = logging.getLogger(__name__)


class NevergradTypeError(Exception):
    pass


def create_instrumentation_variable(parameter):
    """ Create nevergrad.variable from `MCOParameter`. Different
    MCOParameter subclasses have different signature attributes.
    The mapping between MCOParameters and nevergrad types is bijective.

    Parameters
    ----------
    parameter: BaseMCOParameter
        object to convert to nevergrad type

    Returns
    ----------
    nevergrad.Variable
        nevergrad variable of corresponding type
    """
    if hasattr(parameter, "lower_bound") and hasattr(
            parameter, "upper_bound"
    ):
        mid_point = parameter.initial_value
        try:
            _ = parameter.dimension
        except AttributeError:
            parameter_type = ng.p.Scalar
        else:
            parameter_type = ng.p.Array
        return parameter_type(init=mid_point).set_bounds(
            parameter.lower_bound, parameter.upper_bound, method="arctan"
        )
    elif hasattr(parameter, "value"):
        return ng_core.Constant(value=parameter.value)
    elif hasattr(parameter, "levels"):
        return ng.p.TransitionChoice(parameter.sample_values)
    elif hasattr(parameter, "categories"):
        return ng.p.Choice(
            choices=parameter.sample_values, deterministic=True
        )
    else:
        raise NevergradTypeError(
            f"Can not convert {parameter} to any of"
            " supported Nevergrad types"
        )


@provides(IOptimizer)
class NevergradScalarOptimizer(HasStrictTraits):
    """ Optimization of a scalar function using nevergrad.
    """

    #: Algorithms available to work with
    algorithms = Enum(*ng.optimizers.registry.keys())

    #: Optimization budget defines the allowed number of objective calls
    budget = PositiveInt(500)

    def _algorithms_default(self):
        return "TwoPointsDE"

    def optimize_function(self, func, x0, bounds=()):
        """ Minimize the passed function.
        """
        # Create parameterization.
        instrumentation = ng.p.Instrumentation(
            *[create_instrumentation_variable(x) for x in x0]
        )

        # Create optimizer.
        optimizer = ng.optimizers.registry[self.algorithms](
            parametrization=instrumentation, budget=self.budget
        )

        # Optimize.
        optimization_result = optimizer.minimize(func)
        optimal_point = optimization_result.value

        return optimal_point


@provides(IOptimizer)
class NevergradMultiOptimizer(HasStrictTraits):
    """ Optimization of a multi-objective function using nevergrad.
    """

    #: Algorithms available to work with
    algorithms = Enum(*ng.optimizers.registry.keys())

    #: Optimization budget defines the allowed number of objective calls
    budget = PositiveInt(500)

    def _algorithms_default(self):
        return "TwoPointsDE"

    def optimize_function(self, func, x0, bounds=()):
        """ Minimize the passed function.
        """
        # create multi-objective function object
        mfunc = MultiobjectiveFunction(
            multiobjective_function=func,
        )

        # Create parameterization.
        # instrumentation = ng.p.Instrumentation(
        #    *[create_instrumentation_variable(x) for x in x0]
        # )

        # Create optimizer.
        # NOTE: parametrization = instrumentation, DOES NOT WORK
        # for multi-objective function args should be unpacked?
        optimizer = ng.optimizers.registry[self.algorithms](
            parametrization=len(x0), budget=self.budget
        )

        # Optimize.
        optimizer.minimize(mfunc)

        # List of nd.array. Each entry is a member of the Pareto set.
        optimal_points = [x[0][0] for x in mfunc.pareto_front()]

        return optimal_points
