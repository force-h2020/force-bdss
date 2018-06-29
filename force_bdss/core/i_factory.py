from envisage.plugin import Plugin
from traits.api import Interface, Str, Instance


class IFactory(Interface):
    """Envisage required interface for the BaseDataSourceFactory.
    You should not need to use this directly.

    Refer to the BaseDataSourceFactory for documentation.
    """
    id = Str()

    name = Str()

    plugin = Instance(Plugin, allow_none=False)

    def get_name(self):
        pass

    def get_identifier(self):
        pass
