import unittest

from envisage.plugin import Plugin
from traits.trait_errors import TraitError

from force_bdss.tests.dummy_classes.notification_listener import \
    DummyNotificationListenerFactory, DummyNotificationListenerModel, \
    DummyNotificationListener

try:
    import mock
except ImportError:
    from unittest import mock


class TestBaseNotificationListenerFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = mock.Mock(spec=Plugin, id="pid")

    def test_initialization(self):
        factory = DummyNotificationListenerFactory(self.plugin)
        self.assertEqual(factory.id, 'pid.factory.dummy_notification_listener')
        self.assertEqual(factory.name, 'Dummy notification listener')
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
            Broken(self.plugin)

    def test_broken_get_name(self):
        class Broken(DummyNotificationListenerFactory):
            def get_name(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.plugin)

    def test_broken_get_model_class(self):
        class Broken(DummyNotificationListenerFactory):
            def get_model_class(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.plugin)

    def test_broken_get_listener_class(self):
        class Broken(DummyNotificationListenerFactory):
            def get_listener_class(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.plugin)
