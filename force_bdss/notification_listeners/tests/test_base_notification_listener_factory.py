import unittest

import testfixtures
from envisage.plugin import Plugin
from traits.trait_errors import TraitError

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
    def get_name(self):
        return "bar"

    def get_identifier(self):
        return "foo"

    def get_listener_class(self):
        return DummyNotificationListener

    def get_model_class(self):
        return DummyNotificationListenerModel


class TestBaseNotificationListenerFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = mock.Mock(spec=Plugin, id="pid")

    def test_initialization(self):
        factory = DummyNotificationListenerFactory(self.plugin)
        self.assertEqual(factory.id, 'pid.factory.foo')
        self.assertEqual(factory.name, 'bar')
        self.assertEqual(factory.model_class, DummyNotificationListenerModel)
        self.assertEqual(factory.listener_class, DummyNotificationListener)

        self.assertIsInstance(factory.create_model(),
                              DummyNotificationListenerModel)
        self.assertIsInstance(factory.create_listener(),
                              DummyNotificationListener)

    def test_broken_get_identifier(self):
        class Broken(DummyNotificationListenerFactory):
            def get_identifier(self):
                return None

        with self.assertRaises(ValueError):
            factory = Broken(self.plugin)

    def test_broken_get_name(self):
        class Broken(DummyNotificationListenerFactory):
            def get_name(self):
                return None

        with self.assertRaises(TraitError):
            factory = Broken(self.plugin)

    def test_broken_get_model_class(self):
        class Broken(DummyNotificationListenerFactory):
            def get_model_class(self):
                return None

        with self.assertRaises(TraitError):
            factory = Broken(self.plugin)

    def test_broken_get_listener_class(self):
        class Broken(DummyNotificationListenerFactory):
            def get_listener_class(self):
                return None

        with self.assertRaises(TraitError):
            factory = Broken(self.plugin)
