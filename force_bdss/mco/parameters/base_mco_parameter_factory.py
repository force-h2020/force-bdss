from traits.has_traits import HasStrictTraits
from traits.trait_types import String, Type


class BaseMCOParameterFactory(HasStrictTraits):
    """Factory that produces the model instance of a given BASEMCOParameter
    instance.

    Must be reimplemented for the specific parameter."""

    #: A unique string identifying the parameter
    id = String()

    #: A user friendly name (for the UI)
    name = String("Undefined parameter")

    #: A long description of the parameter
    description = String("Undefined parameter")

    # The model class to instantiate when create_model is called.
    model_class = Type('BaseMCOParameter')

    def create_model(self, data_values=None):
        """Creates the instance of the model class and returns it.
        """
        if data_values is None:
            data_values = {}

        return self.model_class(factory=self, **data_values)
