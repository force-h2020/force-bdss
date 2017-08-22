import abc

from traits.api import ABCHasStrictTraits, Instance, String, provides
from envisage.plugin import Plugin

from .i_ui_hooks_factory import IUIHooksFactory


@provides(IUIHooksFactory)
class BaseUIHooksFactory(ABCHasStrictTraits):
    """Base class for notification listeners.
    Notification listeners are extensions that receive event notifications
    from the MCO and perform an associated action.
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
    def create_ui_hook_manager(self):
        """Creates an instance of the hook manager
        The hook manager contains a set of methods that are applicable in
        various moments of the UI application lifetime.

        Returns
        -------
        BaseUIHookManager
        """
