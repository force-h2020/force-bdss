from traits.api import HasStrictTraits, List, String


class DataValue(HasStrictTraits):
    """Contains the parameters as passed from the MCO."""
    #: The user-defined names associated to the values.
    name = List(String)

    #: The CUBA types associated to the values
    type = List(String)

    #: The values as a single array.
    value = Any()

