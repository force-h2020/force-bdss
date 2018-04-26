from traits.api import Interface, String, Instance, Type
from envisage.plugin import Plugin


class IUIHooksFactory(Interface):
    """Envisage required interface for the BaseUIHooksFactory.
    You should not need to use this directly.

    Refer to the BaseUIHooksFactory for documentation.
    """
    id = String()

    name = String()

    ui_hooks_manager_class = Type(
        "force_bdss.ui_hooks.base_ui_hooks_manager.BaseUIHooksManager"
    )

    plugin = Instance(Plugin)

    def create_hook_manager(self):
        """"""
