from traits.api import HasStrictTraits, Any, String


class DataValue(HasStrictTraits):
    """Contains the parameters as passed from the MCO."""
    #: The CUBA types associated to the values
    type = String()

    #: The user-defined names associated to the values.
    name = String()

    #: The values as a single array.
    value = Any()

    def __str__(self):
        return """
        {} {} : {}
        """.format(str(self.type),
                   str(self.name),
                   str(self.value))
