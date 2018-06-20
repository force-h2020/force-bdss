import logging
from traits.api import provides, Type
from envisage.plugin import Plugin

from force_bdss.core.base_factory import BaseFactory
from force_bdss.ui_hooks.base_ui_hooks_manager import BaseUIHooksManager
from .i_ui_hooks_factory import IUIHooksFactory

log = logging.getLogger(__name__)


@provides(IUIHooksFactory)
class BaseUIHooksFactory(BaseFactory):
    """Base class for UIHooksFactory.
    UI Hooks are extensions that perform actions associated to specific
    moments of the UI lifetime.
    """
    #: The UI Hooks manager class to instantiate. Define this to your
    #: base hook managers.
    ui_hooks_manager_class = Type(BaseUIHooksManager, allow_none=False)

    def __init__(self, plugin):
        """Initializes the instance.

        Parameters
        ----------
        plugin: Plugin
            The plugin that holds this factory.
        """
        super(BaseUIHooksFactory, self).__init__(plugin=plugin)

        self.ui_hooks_manager_class = self.get_ui_hooks_manager_class()

    def get_ui_hooks_manager_class(self):
        raise NotImplementedError(
            "get_ui_hooks_manager_class was not implemented "
            "in factory {}".format(
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
