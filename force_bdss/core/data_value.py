from traits.api import HasStrictTraits, Any, String, Enum

from force_bdss.utilities import pop_dunder_recursive


class DataValue(HasStrictTraits):
    """Contains in-transit data between the various components (MCO/DS/KPI).
    Each DataValue instance holds information about the CUBA type it
    contains, the name as assigned by the user, and the value (which can be
    anything.
    """
    #: The CUBA type associated to the value.
    type = String()

    #: The user-defined name associated to the value.
    name = String()

    #: The value.
    value = Any()

    # The numerical accuracy of the value.
    accuracy = Any()

    #: A flag for the quality of the data.
    quality = Enum("AVERAGE", "POOR", "GOOD")

    def __str__(self):

        s = "{} {} = {}".format(
            str(self.type), str(self.name), str(self.value))

        if self.accuracy is not None:
            s += " +/- {}".format(str(self.accuracy))

        s += " ({})".format(str(self.quality))

        return s

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())
