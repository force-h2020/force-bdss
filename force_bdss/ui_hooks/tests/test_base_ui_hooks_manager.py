import unittest

from force_bdss.tests.dummy_classes.ui_hooks import DummyUIHooksManager
from force_bdss.ui_hooks.base_ui_hooks_factory import BaseUIHooksFactory

try:
    import mock
except ImportError:
    from unittest import mock


class TestBaseUIHooksManager(unittest.TestCase):
    def test_initialization(self):
        mock_factory = mock.Mock(spec=BaseUIHooksFactory)
        mgr = DummyUIHooksManager(mock_factory)

        self.assertEqual(mgr.factory, mock_factory)
