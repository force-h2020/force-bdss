import unittest

import testfixtures

from force_bdss.ui_hooks.tests.test_base_ui_hooks_manager import \
    DummyUIHooksManager

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.api import Plugin
from ..base_ui_hooks_factory import BaseUIHooksFactory


class DummyUIHooksFactory(BaseUIHooksFactory):
    def create_ui_hooks_manager(self):
        return DummyUIHooksManager(self)


class DummyUIHooksFactoryFast(BaseUIHooksFactory):
    ui_hooks_manager_class = DummyUIHooksManager


class TestBaseUIHooksFactory(unittest.TestCase):
    def test_initialize(self):
        mock_plugin = mock.Mock(spec=Plugin)
        factory = DummyUIHooksFactory(plugin=mock_plugin)
        self.assertEqual(factory.plugin, mock_plugin)

    def test_fast_definition(self):
        mock_plugin = mock.Mock(spec=Plugin)
        factory = DummyUIHooksFactoryFast(plugin=mock_plugin)

        self.assertIsInstance(
            factory.create_ui_hooks_manager(),
            DummyUIHooksManager)

    def test_fast_definition_errors(self):
        mock_plugin = mock.Mock(spec=Plugin)
        factory = DummyUIHooksFactoryFast(plugin=mock_plugin)
        factory.ui_hooks_manager_class = None

        with testfixtures.LogCapture():
            with self.assertRaises(RuntimeError):
                factory.create_ui_hooks_manager()
