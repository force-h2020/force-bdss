import unittest

from force_bdss.ui_hooks.base_ui_hooks_factory import BaseUIHooksFactory
from force_bdss.ui_hooks.base_ui_hooks_manager import BaseUIHooksManager

try:
    import mock
except ImportError:
    from unittest import mock


class DummyUIHooksManager(BaseUIHooksManager):
    pass


class TestBaseUIHooksManager(unittest.TestCase):
    def test_initialization(self):
        mock_factory = mock.Mock(spec=BaseUIHooksFactory)
        mgr = DummyUIHooksManager(mock_factory)

        self.assertEqual(mgr.factory, mock_factory)
