from traits.api import HasStrictTraits, String, Type, Instance


class BaseMCOParameterFactory(HasStrictTraits):
    id = String()
    name = String("Undefined parameter")
    description = String("Undefined parameter")
    model_class = Type('BaseMCOParameter')

    def create_model(self, data_values=None):
        if data_values is None:
            data_values = {}

        return self.model_class(factory=self, **data_values)


class BaseMCOParameter(HasStrictTraits):
    factory = Instance(BaseMCOParameterFactory)
    value_name = String()
    value_type = String()
