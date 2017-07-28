from traits.api import HasTraits, Array, ArrayOrNone, List, String, Instance

from .base_data_source import BaseDataSource


class DataSourceResult(HasTraits):
    """Represents the result of a DataSource evaluation.

    Note
    ----
    Difference between accuracy and quality:
      - uncertainty is a numerical quantity defining the accuracy of the value.
        For example, a pressure can be 10.4 +/- 0.1, with 0.1 being the
        accuracy
      - quality is the level of importance and reliability of that value.
        It should be considered as a weight of how much trust one should hold
        on this information.
    """

    #: A reference to the DataSource that computed this result.
    originator = Instance(BaseDataSource)

    #: The user-defined names associated to each result.
    value_names = List(String)

    #: The CUBA types of each value.
    value_types = List(String)

    #: The values for each entry. Note that this is a NxM array, allowing
    #: to propagate more than single scalar values associated to a given value.
    values = Array(shape=(None, None))

    #: If present, the numerical accuracy of the above values.
    accuracy = ArrayOrNone(shape=(None, None))

    #: If present, the assessed quality of the above values.
    quality = ArrayOrNone(shape=(None, None))

    def __str__(self):
        return """
        DataSourceResults

        originator:
        {}

        value_names:
        {}

        value_types:
        {}

        values:
        {}

        Accuracy:
        {}

        Quality:
        {}
        """.format(
            self.originator,
            self.value_names,
            self.value_types,
            self.values,
            self.accuracy,
            self.quality)
