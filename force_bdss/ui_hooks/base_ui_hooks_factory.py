import logging
from traits.api import HasStrictTraits, Instance, Str, provides, Type
from envisage.plugin import Plugin

from force_bdss.ids import factory_id
from force_bdss.ui_hooks.base_ui_hooks_manager import BaseUIHooksManager
from .i_ui_hooks_factory import IUIHooksFactory

log = logging.getLogger(__name__)


@provides(IUIHooksFactory)
class BaseUIHooksFactory(HasStrictTraits):
    """Base class for UIHooksFactory.
    UI Hooks are extensions that perform actions associated to specific
    moments of the UI lifetime.
    """
    #: identifier of the factory
    id = Str()

    #: Name of the factory. User friendly for UI
    name = Str()

    #: The UI Hooks manager class to instantiate. Define this to your
    #: base hook managers.
    ui_hooks_manager_class = Type(BaseUIHooksManager, allow_none=False)

    #: A reference to the containing plugin
    plugin = Instance(Plugin, allow_none=False)

    def __init__(self, plugin, *args, **kwargs):
        """Initializes the instance.

        Parameters
        ----------
        plugin: Plugin
            The plugin that holds this factory.
        """
        self.plugin = plugin
        super(BaseUIHooksFactory, self).__init__(*args, **kwargs)

        self.ui_hooks_manager_class = self.get_ui_hooks_manager_class()
        self.name = self.get_name()
        identifier = self.get_identifier()
        try:
            id = factory_id(self.plugin.id, identifier)
        except ValueError:
            raise ValueError(
                "Invalid identifier {} returned by "
                "{}.get_identifier()".format(
                    identifier,
                    self.__class__.__name__
                )
            )
        self.id = id

    def get_ui_hooks_manager_class(self):
        raise NotImplementedError(
            "get_ui_hooks_manager_class was not implemented "
            "in factory {}".format(
                self.__class__))

    def get_name(self):
        raise NotImplementedError(
            "get_name was not implemented in factory {}".format(
                self.__class__))

    def get_identifier(self):
        raise NotImplementedError(
            "get_identifier was not implemented in factory {}".format(
                self.__class__))

    def create_ui_hooks_manager(self):
        """Creates an instance of the hook manager.
        The hooks manager contains a set of methods that are applicable in
        various moments of the UI application lifetime.

        Returns
        -------
        BaseUIHooksManager
        """
        return self.ui_hooks_manager_class(self)
