import logging
from traits.api import ABCHasStrictTraits, Instance, String, provides
from envisage.plugin import Plugin

from force_bdss.ui_hooks.base_ui_hooks_manager import BaseUIHooksManager
from .i_ui_hooks_factory import IUIHooksFactory

log = logging.getLogger(__name__)


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

    #: The UI Hooks manager class to instantiate. Define this to your
    #: base hook managers.
    ui_hooks_manager_class = Instance(BaseUIHooksManager)

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

    def create_ui_hooks_manager(self):
        """Creates an instance of the hook manager.
        The hooks manager contains a set of methods that are applicable in
        various moments of the UI application lifetime.

        Returns
        -------
        BaseUIHooksManager
        """
        if self.ui_hooks_manager_class is None:
            msg = ("ui_hooks_manager_class cannot be None in {}. Either "
                   "define ui_hooks_manager_class or reimplement "
                   "create_ui_hooks_manager on "
                   "your factory class.".format(self.__class__.__name__))
            log.error(msg)
            raise RuntimeError(msg)

        return self.ui_hooks_manager_class(self)
