from traits.api import HasStrictTraits, Bool

from ..local_traits import Identifier


class OutputSlotInfo(HasStrictTraits):
    """
    Class that specifies the name and characteristics of the output slots
    of a data source.
    This entity will go in the model object, and associates the positional
    order in the containing list with the variable name that refers to the
    value that should be taken.
    """
    #: The user defined name of the variable containing the value.
    name = Identifier()

    #: True if the value associated to this output slot must be exported as
    #: a KPI.
    kpi = Bool(False)
