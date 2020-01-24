from traits.api import HasStrictTraits

from force_bdss.core.verifier import VerifierError
from force_bdss.core.base_model import pop_dunder_recursive
from force_bdss.local_traits import Identifier


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

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())
