from traits.api import Interface, Unicode


class IFactory(Interface):
    """Envisage required interface for the BaseDataSourceFactory.
    You should not need to use this directly.

    Refer to the BaseDataSourceFactory for documentation.
    """
    id = Unicode()

    name = Unicode()

    plugin_id = Unicode(allow_none=False)

    def get_name(self):
        pass

    def get_identifier(self):
        pass
