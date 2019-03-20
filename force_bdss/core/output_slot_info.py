from traits.api import HasStrictTraits

from ..local_traits import Identifier
from force_bdss.io.workflow_writer import pop_dunder_recursive


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

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())
