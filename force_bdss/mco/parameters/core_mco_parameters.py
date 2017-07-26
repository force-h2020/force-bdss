from traits.api import Float

from ...ids import mco_parameter_id
from .base_mco_parameter import BaseMCOParameter
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory


class RangedMCOParameter(BaseMCOParameter):
    """Expresses a MCO parameter that has a range between two floating
    point values."""
    initial_value = Float()
    lower_bound = Float()
    upper_bound = Float(1)


class RangedMCOParameterFactory(BaseMCOParameterFactory):
    """The factory of the above model"""
    id = mco_parameter_id("enthought", "ranged")
    model_class = RangedMCOParameter
    name = "Range"
    description = "A ranged parameter in floating point values."


def all_core_factories():
    """Produces a list of all factories contained in this module."""
    import inspect

    return [c()
            for c in inspect.getmodule(all_core_factories).__dict__.values()
            if inspect.isclass(c) and
            c is not BaseMCOParameterFactory and
            issubclass(c, BaseMCOParameterFactory)]
