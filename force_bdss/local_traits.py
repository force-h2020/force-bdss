from traits.api import Regex, String

#: Used for variable names, but allow also empty string as it's the default
#: case and it will be present if the workflow is saved before actually
#: specifying the value.
Identifier = Regex(regex="(^[^\d\W]\w*\Z|^\Z)")

#: Identifies a CUBA type with its key. At the moment a String with
#: no validation, but will come later.
CUBAType = String()
