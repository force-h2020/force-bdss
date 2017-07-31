from traits.api import HasStrictTraits, String


class Slot(HasStrictTraits):
    """Describes an input or output slot in the DataSource or
    KPICalculator"""
    #: A textual description of the slot
    description = String("No description")

    #: The CUBA key of the slot
    value_type = String()

