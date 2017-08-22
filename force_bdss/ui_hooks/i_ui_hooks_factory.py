from traits.api import Interface, String, Instance
from envisage.plugin import Plugin


class IUIHooksFactory(Interface):
    """Envisage required interface for the BaseUIHooksFactory.
    You should not need to use this directly.

    Refer to the BaseUIHooksFactory for documentation.
    """
    id = String()

    name = String()

    plugin = Instance(Plugin)

    def create_hook_manager(self):
        """"""
