from traits.api import HasStrictTraits, Unicode

from force_bdss.io.workflow_writer import pop_dunder_recursive
from force_bdss.local_traits import Identifier, CUBAType
from force_bdss.core.verifier import VerifierError


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

    def _verify_name(self, slot_title="", verification_severity="error"):
        """ Verifies that the `name` trait of the SlotInfo object is defined,
        as it may be required for a later execution layer.

        Parameters
        --------
        slot_title: str
            The SlotInfo title, which specifies the meta-type of the slot
        verification_severity: str
            The `severity` of the potential VerifierError
        """

        errors = []
        if not self.name:
            error = VerifierError(
                subject=self,
                severity=verification_severity,
                trait_name="name",
                global_error="An {} variable has an undefined name".format(
                    slot_title
                ),
            )
            errors.append(error)

        return errors
