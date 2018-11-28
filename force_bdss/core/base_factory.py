from envisage.plugin import Plugin
from traits.api import Bool, HasStrictTraits, Unicode, Instance

from force_bdss.ids import factory_id


class BaseFactory(HasStrictTraits):
    #: Unique identifier that identifies the factory uniquely in the
    #: universe of factories. Create one with the function factory_id()
    id = Unicode()

    #: A human readable name of the factory. Spaces allowed
    name = Unicode()

    #: A long description of the factory.
    description = Unicode()

    #: If the factor should be visible in the UI. Set to false to make it
    #: invisible. This is normally useful for notification systems that are
    #: not supposed to be configured by the user.
    ui_visible = Bool(True)

    #: Reference to the plugin that carries this factory
    #: This is automatically set by the system. you should not define it
    #: in your subclass.
    plugin = Instance(Plugin, allow_none=False)

    def __init__(self, plugin, *args, **kwargs):
        super(BaseFactory, self).__init__(plugin=plugin, *args, **kwargs)

        self.name = self.get_name()
        self.description = self.get_description()
        identifier = self.get_identifier()
        try:
            id = self._global_id(identifier)
        except ValueError:
            raise ValueError(
                "Invalid identifier {} returned by "
                "{}.get_identifier()".format(
                    identifier,
                    self.__class__.__name__
                )
            )
        self.id = id

    def get_name(self):
        """Must be reimplemented to return a user-visible name of the
        data source.
        """
        raise NotImplementedError(
            "get_name was not implemented in factory {}".format(
                self.__class__))

    def get_identifier(self):
        """Must be reimplemented to return a unique string identifying
        the factory. The provider is responsible to guarantee this identifier
        to be unique across the plugin data sources.
        """
        raise NotImplementedError(
            "get_identifier was not implemented in factory {}".format(
                self.__class__))

    def get_description(self):
        return "No description available."

    def _global_id(self, identifier):
        return factory_id(self.plugin.id, identifier)
