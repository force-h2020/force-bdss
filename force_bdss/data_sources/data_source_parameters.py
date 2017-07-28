from traits.api import HasStrictTraits, Array, List, String


class DataSourceParameters(HasStrictTraits):
    """Contains the parameters as passed from the MCO."""
    #: The user-defined names associated to the values.
    value_names = List(String)

    #: The CUBA types associated to the values
    value_types = List(String)

    #: The values as a single array.
    values = Array(shape=(None,))

    def __str__(self):
        return """
        DataSourceParameters
        value_names:
        {}
        value_types:
        {}
        values:
        {}
        """.format(str(self.value_names),
                   str(self.value_types),
                   str(self.values))
