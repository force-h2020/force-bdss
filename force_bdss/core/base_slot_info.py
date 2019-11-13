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

    #: Slot Info title
    _title = ""

    #: Slot state verification severity
    _verification_severity = "error"

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())

    def verify(self):
        """ BaseSlotInfo may require a non-empty name trait to be used in a
        later execution layer. However, not all outputs are required to be
        used in later stages.

        Parameters:
        title: str
            Title of the SlotInfo ("Input", "Output")
        severity: str
            Severity of the verification error
        """

        errors = []
        if not self.name:
            error = VerifierError(
                subject=self,
                severity=self._verification_severity,
                trait_name="name",
                global_error="An {} variable has an undefined name".format(
                    self._title
                ),
            )
            errors.append(error)

        return errors
