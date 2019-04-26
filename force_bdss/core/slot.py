from traits.api import HasStrictTraits, Unicode
from ..local_traits import CUBAType
from force_bdss.io.workflow_writer import pop_dunder_recursive


class Slot(HasStrictTraits):
    """
    Describes an input or output slot in the DataSource or
    KPICalculator. If the DataSource and KPICalculator are functions, slots
    define their argument number and types they need as input and what
    they return as output.
    """
    #: A textual description of the slot
    description = Unicode("No description")

    #: The CUBA key of the slot
    type = CUBAType()

    #: A default name for the slot item
    name = Unicode("")

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())
