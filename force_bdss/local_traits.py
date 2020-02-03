from traits.api import Regex, BaseInt

#: Used for variable names, but allow also empty string as it's the default
#: case and it will be present if the workflow is saved before actually
#: specifying the value.
Identifier = Regex(regex=r"(^[^\d\W]\w*\Z|^\Z)")


class PositiveInt(BaseInt):
    """A positive integer trait."""

    info_text = 'a positive integer'

    default_value = 1

    def validate(self, object, name, value):
        int_value = super(PositiveInt, self).validate(object, name, value)

        if int_value > 0:
            return int_value

        self.error(object, name, value)
