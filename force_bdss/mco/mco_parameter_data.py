from traits.api import HasStrictTraits, Any, String


class MCOParameterData(HasStrictTraits):
    """Contains the parameters as passed from the MCO."""
    #: The user-defined name associated to the value.
    value_name = String()

    #: The CUBA type associated to the value
    value_type = String()

    #: The value.
    value = Any()

    def __str__(self):
        return """
        MCOParameterData
        value_name:
        {}
        value_type:
        {}
        value:
        {}
        """.format(str(self.value_name),
                   str(self.value_type),
                   str(self.value))
