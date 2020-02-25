from traits.api import String, Instance

from force_bdss.core.base_model import BaseModel
from force_bdss.core.verifier import VerifierError
from force_bdss.mco.parameters.base_mco_parameter_factory import (
    BaseMCOParameterFactory,
)
from force_bdss.local_traits import Identifier


class BaseMCOParameter(BaseModel):
    """The base class of all MCO Parameter models.
    Must be reimplemented by specific classes handling the specific parameter
    that MCOs understand.
    """

    #: The generating factory. Used to retrieve the ID at serialization.
    factory = Instance(BaseMCOParameterFactory, visible=False, transient=True)

    #: A user defined name for the parameter
    name = Identifier(visible=False, verify=True)

    #: A CUBA key describing the type of the parameter
    type = String(visible=False, verify=True)

    def __init__(self, factory, *args, **kwargs):
        super().__init__(factory=factory, *args, **kwargs)

    def verify(self):
        """ Verify the MCO parameter.

        Check that the MCO parameter:
        - has a name
        - has a type

        Returns
        -------
        errors : list of VerifierErrors
            The list of all detected errors in the parameter.
        """
        errors = []
        if not self.name:
            errors.append(
                VerifierError(
                    subject=self,
                    trait_name="name",
                    local_error="MCO parameter is not named",
                    global_error="An MCO parameter is not named",
                )
            )
        if not self.type:
            errors.append(
                VerifierError(
                    subject=self,
                    trait_name="type",
                    local_error="MCO parameter has no type set",
                    global_error="An MCO parameter has no type set",
                )
            )
        return errors

    @classmethod
    def from_json(cls, factory, json_data):
        parameter = factory.create_model(json_data)
        return parameter
