#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import HasStrictTraits, Enum

from force_bdss.local_traits import Identifier
from force_bdss.utilities import pop_dunder_recursive

from .verifier import VerifierError


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

    def verify(self):
        """ Verify that the InputSlotInfo is valid. """
        errors = []
        if not self.name:
            errors.append(
                VerifierError(
                    subject=self,
                    local_error="Input slot is not named",
                    global_error="An input slot is not named",
                )
            )
        return errors

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())
