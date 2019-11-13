from force_bdss.core.verifier import VerifierError

from .base_slot_info import BaseSlotInfo


class OutputSlotInfo(BaseSlotInfo):
    """
    Class that specifies the name and characteristics of the output slots
    of a data source.
    """

    def verify(self):
        """ OutputSlotInfo require a non-empty name to be used in a later
        execution layer. However, not all outputs are required to be used in
        later stages."""
        errors = []
        if not self.name:
            errors.append(
                VerifierError(
                    severity='warning', subject=self, trait_name='name',
                    global_error='An output variable has an undefined name'
                )
            )

        return errors
