
import unittest

from envisage.plugin import Plugin

from force_bdss.core_plugins.dummy.dummy_notification_listener\
    .dummy_notification_listener_factory import \
    DummyNotificationListenerFactory

try:
    import mock
except ImportError:
    from unittest import mock


class TestDummyNotificationListenerFactory(unittest.TestCase):
    def test_create_methods(self):
        factory = DummyNotificationListenerFactory(mock.Mock(spec=Plugin))
        model = factory.create_model()
        self.assertEqual(model.factory, factory)

        listener = factory.create_listener()
        self.assertEqual(listener.factory, factory)
