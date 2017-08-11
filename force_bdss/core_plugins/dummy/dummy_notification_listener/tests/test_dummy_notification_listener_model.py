import unittest

from force_bdss.core_plugins.dummy.dummy_notification_listener\
    .dummy_notification_listener_factory import \
    DummyNotificationListenerFactory
from force_bdss.core_plugins.dummy.dummy_notification_listener\
    .dummy_notification_listener_model import \
    DummyNotificationListenerModel

try:
    import mock
except ImportError:
    from unittest import mock


class TestDummyNotificationListenerModel(unittest.TestCase):
    def test_initialization(self):
        factory = mock.Mock(spec=DummyNotificationListenerFactory)
        model = DummyNotificationListenerModel(factory)
        self.assertEqual(model.factory, factory)
