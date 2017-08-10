import re
from traits.api import Regex, BaseStr, String

#: Used for variable names, but allow also empty string as it's the default
#: case and it will be present if the workflow is saved before actually
#: specifying the value.
Identifier = Regex(regex="(^[^\d\W]\w*\Z|^\Z)")


class ZMQSocketURL(BaseStr):
    def validate(self, object, name, value):
        super(ZMQSocketURL, self).validate(object, name, value)
        m = re.match(
            "tcp://(\\d{1,3})\.(\\d{1,3})\.(\\d{1,3})\.(\\d{1,3}):(\\d+)",
            value)
        if m is None:
            self.error(object, name, value)

        a, b, c, d, port = m.groups()

        if not all(map(lambda x: 0 <= int(x) <= 255, (a, b, c, d))):
            self.error(object, name, value)

        if not (1 <= int(port) <= 65535):
            self.error(object, name, value)

        return value


#: Identifies a CUBA type with its key. At the moment a String with
#: no validation, but will come later.
CUBAType = String()
