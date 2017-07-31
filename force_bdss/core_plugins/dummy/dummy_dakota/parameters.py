from traits.api import Float

from force_bdss.ids import mco_parameter_id
from force_bdss.mco.parameters.base_mco_parameter import BaseMCOParameter
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory


class RangedMCOParameter(BaseMCOParameter):
    """Expresses a MCO parameter that has a range between two floating
    point values."""
    initial_value = Float(0.0)
    lower_bound = Float(0.0)
    upper_bound = Float(1.0)


class RangedMCOParameterFactory(BaseMCOParameterFactory):
    """The factory of the above model"""
    id = mco_parameter_id("enthought", "dummy_dakota", "ranged")
    model_class = RangedMCOParameter
    name = "Range"
    description = "A ranged parameter in floating point values."
