from traits.api import Enum

from force_bdss.core.verifier import VerifierError

from .base_slot_info import BaseSlotInfo


class InputSlotInfo(BaseSlotInfo):
    """
    Class that specifies the name and characteristics of the input slots
    of a data source.
    """

    #: Where the value will come from.
    #: At the moment, only the Environment is supported: the source is the
    #: parameter in the current execution environment with the name specified
    #: as ``name``.
    source = Enum('Environment')

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
