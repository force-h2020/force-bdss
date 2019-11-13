from traits.api import HasStrictTraits, Unicode

from force_bdss.io.workflow_writer import pop_dunder_recursive
from force_bdss.local_traits import Identifier, CUBAType


class BaseSlotInfo(HasStrictTraits):
    """
    Class that specifies the origin of data for the slots of a data source
    or KPI calculator.
    This entity will go in the model object, and associates the positional
    order in the containing list with the variable name that refers to the
    value that should be taken.
    """

    #: The user defined name of the variable containing the value.
    name = Identifier()

    #: The CUBA key of the slot
    type = CUBAType()

    #: A textual description of the slot
    description = Unicode("No description")

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())
