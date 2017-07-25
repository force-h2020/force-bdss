from traits.has_traits import HasStrictTraits
from traits.trait_types import String, Type


class BaseMCOParameterFactory(HasStrictTraits):
    id = String()
    name = String("Undefined parameter")
    description = String("Undefined parameter")
    model_class = Type('BaseMCOParameter')

    def create_model(self, data_values=None):
        if data_values is None:
            data_values = {}

        return self.model_class(factory=self, **data_values)
