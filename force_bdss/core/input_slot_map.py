from traits.api import HasStrictTraits, Enum, String


class InputSlotMap(HasStrictTraits):
    """Class that specifies the origin of data for the slots of a data source.
    """
    #: If MCO, the source is the MCO parameter with name specified at
    #: value_name. If Fixed, the value specified in "value" will be used
    #: instead.
    source = Enum('MCO', 'Fixed')
    name = String()
    value = String()
