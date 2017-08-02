from traits.api import Regex

#: Used for variable names, but allow also empty string as it's the default
#: case and it will be present if the workflow is saved before actually
#: specifying the value.
Identifier = Regex(regex="(^[^\d\W]\w*\Z|^\Z)")
