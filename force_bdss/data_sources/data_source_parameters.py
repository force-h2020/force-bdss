from traits.api import HasStrictTraits, Array, List, String


class DataSourceParameters(HasStrictTraits):
    value_types = List(String)
    values = Array(shape=(None,))

    def __str__(self):
        return """
        DataSourceParameters
        value_types:
        {}
        values:
        {}
        """.format(str(self.value_types), str(self.values))
