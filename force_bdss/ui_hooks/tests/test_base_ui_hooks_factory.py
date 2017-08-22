import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.api import Plugin
from ..base_ui_hooks_factory import BaseUIHooksFactory


class NullUIHooksFactory(BaseUIHooksFactory):
    def create_ui_hooks_manager(self):
        return None


class TestBaseUIHooksFactory(unittest.TestCase):
    def test_initialize(self):
        mock_plugin = mock.Mock(spec=Plugin)
        factory = NullUIHooksFactory(plugin=mock_plugin)
        self.assertEqual(factory.plugin, mock_plugin)
