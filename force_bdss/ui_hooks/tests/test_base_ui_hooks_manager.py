import unittest

from ..base_ui_hooks_manager import BaseUIHooksManager
from ..base_ui_hooks_factory import BaseUIHooksFactory
try:
    import mock
except ImportError:
    from unittest import mock


class TestBaseUIHookManager(unittest.TestCase):
    def test_initialization(self):
        mock_factory = mock.Mock(spec=BaseUIHooksFactory)
        mgr = BaseUIHooksManager(mock_factory)

        self.assertEqual(mgr.factory, mock_factory)
