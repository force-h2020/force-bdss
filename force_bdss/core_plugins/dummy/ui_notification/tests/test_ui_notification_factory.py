import unittest

from envisage.plugin import Plugin

from force_bdss.core_plugins.dummy.ui_notification.ui_notification import \
    UINotification
from force_bdss.core_plugins.dummy.ui_notification.ui_notification_factory \
    import \
    UINotificationFactory
from force_bdss.core_plugins.dummy.ui_notification.ui_notification_model \
    import \
    UINotificationModel

try:
    import mock
except ImportError:
    from unittest import mock


class TestUINotificationFactory(unittest.TestCase):
    def test_initialization(self):
        factory = UINotificationFactory(mock.Mock(spec=Plugin))
        self.assertEqual(
            factory.id,
            "force.bdss.enthought.factory.ui_notification")

    def test_create_model(self):
        factory = UINotificationFactory(mock.Mock(spec=Plugin))
        model = factory.create_model()
        self.assertIsInstance(model, UINotificationModel)
        self.assertEqual(model.factory, factory)

        model = factory.create_model({})
        self.assertIsInstance(model, UINotificationModel)
        self.assertEqual(model.factory, factory)

    def test_create_listener(self):
        factory = UINotificationFactory(mock.Mock(spec=Plugin))
        listener = factory.create_listener()
        self.assertIsInstance(listener, UINotification)
