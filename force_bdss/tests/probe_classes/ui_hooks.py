try:
    import mock
except ImportError:
    from unittest import mock

from envisage.api import Plugin

from traits.api import Bool
from force_bdss.api import BaseUIHooksFactory, BaseUIHooksManager


class ProbeUIHooksManager(BaseUIHooksManager):
    before_execution_called = Bool()
    after_execution_called = Bool()
    before_save_called = Bool()

    # Set this one to raise an exception in the methods
    before_execution_raises = Bool(False)
    after_execution_raises = Bool(False)
    before_save_raises = Bool(False)

    def before_execution(self, task):
        self.before_execution_called = True
        if self.before_execution_raises:
            raise Exception("Boom")

    def after_execution(self, task):
        self.after_execution_called = True
        if self.after_execution_raises:
            raise Exception("Boom")

    def before_save(self, task):
        self.before_save_called = True
        if self.before_save_raises:
            raise Exception("Boom")


class ProbeUIHooksFactory(BaseUIHooksFactory):
    create_ui_hooks_manager_raises = Bool()

    def __init__(self, plugin=None, *args, **kwargs):
        if plugin is None:
            plugin = mock.Mock(Plugin)

        super(ProbeUIHooksFactory, self).__init__(
            plugin=plugin, *args, **kwargs)

    def create_ui_hooks_manager(self):
        if self.create_ui_hooks_manager_raises:
            raise Exception("Boom")

        return ProbeUIHooksManager(self)
