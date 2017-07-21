from traits.api import HasStrictTraits, Array, List, String


class DataSourceParameters(HasStrictTraits):
    value_names = List(String)
    value_types = List(String)
    values = Array(shape=(None,))
