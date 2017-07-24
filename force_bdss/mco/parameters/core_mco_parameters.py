from traits.api import Float

from ...ids import mco_parameter_id
from .base_mco_parameter import BaseMCOParameter, BaseMCOParameterFactory


class RangedMCOParameter(BaseMCOParameter):
    initial_value = Float()
    upper_bound = Float()
    lower_bound = Float()


class RangedMCOParameterFactory(BaseMCOParameterFactory):
    id = mco_parameter_id("enthought", "ranged")
    model_class = RangedMCOParameter
    name = "Range"
    description = "A ranged parameter in floating point values."


def all_core_factories():
    import inspect

    return [c for c in inspect.getmodule(all_core_factories).__dict__.values()
            if inspect.isclass(c) and issubclass(c, BaseMCOParameterFactory)]
