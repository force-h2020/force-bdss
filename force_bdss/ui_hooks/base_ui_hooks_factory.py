import abc

from traits.api import ABCHasStrictTraits, Instance, String, provides
from envisage.plugin import Plugin

from .i_ui_hooks_factory import IUIHooksFactory


@provides(IUIHooksFactory)
class BaseUIHooksFactory(ABCHasStrictTraits):
    """Base class for UIHooksFactory.
    UI Hooks are extensions that perform actions associated to specific
    moments of the UI lifetime.
    """
    #: identifier of the factory
    id = String()

    #: Name of the factory. User friendly for UI
    name = String()

    #: A reference to the containing plugin
    plugin = Instance(Plugin)

    def __init__(self, plugin, *args, **kwargs):
        """Initializes the instance.

        Parameters
        ----------
        plugin: Plugin
            The plugin that holds this factory.
        """
        self.plugin = plugin
        super(BaseUIHooksFactory, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def create_ui_hooks_manager(self):
        """Creates an instance of the hook manager.
        The hooks manager contains a set of methods that are applicable in
        various moments of the UI application lifetime.

        Returns
        -------
        BaseUIHooksManager
        """
