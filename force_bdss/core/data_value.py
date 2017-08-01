from traits.api import HasStrictTraits, Any, String, Int


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

    accuracy = Any()

    quality = Int()

    def __str__(self):
        return """
        {} {} : {}
        """.format(str(self.type),
                   str(self.name),
                   str(self.value))
