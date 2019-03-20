from traits.api import HasStrictTraits, Enum

from ..local_traits import Identifier
from force_bdss.io.workflow_writer import pop_dunder_recursive


class InputSlotInfo(HasStrictTraits):
    """
    Class that specifies the origin of data for the slots of a data source
    or KPI calculator.
    This entity will go in the model object, and associates the positional
    order in the containing list with the variable name that refers to the
    value that should be taken.
    """
    #: Where the value will come from.
    #: At the moment, only the Environment is supported: the source is the
    #: parameter in the current execution environment with the name specified
    #: as ``name``.
    source = Enum('Environment')

    #: The user defined name of the variable containing the value.
    name = Identifier()

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())
