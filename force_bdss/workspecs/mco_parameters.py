from traits.api import HasStrictTraits, String, Float


class MCOParameter(HasStrictTraits):
    pass


class RangedMCOParameter(MCOParameter):
    name = String()
    value_type = String()
    initial_value = Float()
    upper_bound = Float()
    lower_bound = Float()
