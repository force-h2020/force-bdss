from traits.api import Interface, Str


class IFactory(Interface):
    """Envisage required interface for the BaseDataSourceFactory.
    You should not need to use this directly.

    Refer to the BaseDataSourceFactory for documentation.
    """
    id = Str()

    name = Str()

    plugin_id = Str(allow_none=False)

    def get_name(self):
        """
        :return: factory name.
        """

    def get_identifier(self):
        """
        :return: factory UID
        """
