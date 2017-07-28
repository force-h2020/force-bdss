from traits.api import HasStrictTraits, String, Type, Instance

from ..base_mco_bundle import BaseMCOBundle


class BaseMCOParameterFactory(HasStrictTraits):
    """Factory that produces the model instance of a given BASEMCOParameter
    instance.

    Must be reimplemented for the specific parameter."""

    bundle = Instance(BaseMCOBundle)

    #: A unique string identifying the parameter
    id = String()

    #: A user friendly name (for the UI)
    name = String("Undefined parameter")

    #: A long description of the parameter
    description = String("Undefined parameter")

    # The model class to instantiate when create_model is called.
    model_class = Type('BaseMCOParameter')

    def __init__(self, bundle):
        self.bundle = bundle
        super(BaseMCOParameterFactory, self).__init__()

    def create_model(self, data_values=None):
        """Creates the instance of the model class and returns it.
        """
        if data_values is None:
            data_values = {}

        return self.model_class(factory=self, **data_values)
