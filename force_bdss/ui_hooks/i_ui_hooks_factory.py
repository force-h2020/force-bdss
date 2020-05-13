#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Type

from force_bdss.core.i_factory import IFactory


class IUIHooksFactory(IFactory):
    """Envisage required interface for the BaseUIHooksFactory.
    You should not need to use this directly.

    Refer to the BaseUIHooksFactory for documentation.
    """
    ui_hooks_manager_class = Type(
        "force_bdss.ui_hooks.base_ui_hooks_manager.BaseUIHooksManager",
        allow_none=False
    )

    def get_ui_hooks_manager_class(self):
        """
        :return:  hooks manager class
        """

    def create_ui_hooks_manager(self):
        """
        :return: hooks manager
        """
