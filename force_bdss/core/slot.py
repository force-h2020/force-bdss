#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import HasStrictTraits, Str

from force_bdss.local_traits import CUBAType
from force_bdss.utilities import pop_dunder_recursive


class Slot(HasStrictTraits):
    """
    Describes an input or output slot in the DataSource or
    KPICalculator. If the DataSource and KPICalculator are functions, slots
    define their argument number and types they need as input and what
    they return as output.
    """
    #: A textual description of the slot
    description = Str("No description")

    #: The CUBA key of the slot
    type = CUBAType()

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())
