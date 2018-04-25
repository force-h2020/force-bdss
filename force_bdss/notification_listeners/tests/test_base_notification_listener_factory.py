import unittest

import testfixtures
from envisage.plugin import Plugin

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.notification_listeners.base_notification_listener import \
    BaseNotificationListener
from force_bdss.notification_listeners.base_notification_listener_factory \
    import \
    BaseNotificationListenerFactory
from force_bdss.notification_listeners.base_notification_listener_model \
    import \
    BaseNotificationListenerModel


class DummyNotificationListener(BaseNotificationListener):
    def deliver(self, event):
        pass


class DummyNotificationListenerModel(BaseNotificationListenerModel):
    pass


class DummyNotificationListenerFactory(BaseNotificationListenerFactory):
    id = "foo"

    name = "bar"

    def create_listener(self):
        return DummyNotificationListener(self)

    def create_model(self, model_data=None):
        return DummyNotificationListenerModel(self)


class DummyNotificationListenerFactoryFast(BaseNotificationListenerFactory):
    id = "foo"

    name = "bar"

    listener_class = DummyNotificationListener

    model_class = DummyNotificationListenerModel


class TestBaseNotificationListenerFactory(unittest.TestCase):
    def test_initialization(self):
        factory = DummyNotificationListenerFactory(mock.Mock(spec=Plugin))
        self.assertEqual(factory.id, 'foo')
        self.assertEqual(factory.name, 'bar')

    def test_fast_definition(self):
        factory = DummyNotificationListenerFactoryFast(mock.Mock(spec=Plugin))

        self.assertIsInstance(factory.create_listener(),
                              DummyNotificationListener)

        self.assertIsInstance(factory.create_model(),
                              DummyNotificationListenerModel)

    def test_fast_definition_errors(self):
        factory = DummyNotificationListenerFactoryFast(mock.Mock(spec=Plugin))
        factory.listener_class = None
        factory.model_class = None

        with testfixtures.LogCapture():
            with self.assertRaises(RuntimeError):
                factory.create_model()

            with self.assertRaises(RuntimeError):
                factory.create_listener()
