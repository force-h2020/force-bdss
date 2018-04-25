from traits.api import Interface, String, Instance
from envisage.plugin import Plugin

from force_bdss.ui_hooks.base_ui_hooks_manager import BaseUIHooksManager


class IUIHooksFactory(Interface):
    """Envisage required interface for the BaseUIHooksFactory.
    You should not need to use this directly.

    Refer to the BaseUIHooksFactory for documentation.
    """
    id = String()

    name = String()

    ui_hooks_manager_class = Instance(BaseUIHooksManager)

    plugin = Instance(Plugin)

    def create_hook_manager(self):
        """"""
