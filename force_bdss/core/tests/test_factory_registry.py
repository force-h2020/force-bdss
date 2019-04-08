import unittest
import warnings

from force_bdss.ids import factory_id, mco_parameter_id
from force_bdss.tests.dummy_classes.extension_plugin import (
    DummyDataSourceFactory, DummyExtensionPlugin, DummyMCOFactory,
    DummyNotificationListenerFactory
)

from force_bdss.core.factory_registry import FactoryRegistry


class TestFactoryRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = FactoryRegistry()

    def test_initialization(self):
        self.assertEqual(self.registry.mco_factories, [])
        self.assertEqual(self.registry.data_source_factories, [])


class TestFactoryRegistryWithContent(unittest.TestCase):
    def setUp(self):
        self.plugin = DummyExtensionPlugin()
        self.plugin.start()
        self.registry = FactoryRegistry(
            mco_factories=[DummyMCOFactory(plugin=self.plugin)],
            data_source_factories=[DummyDataSourceFactory(plugin=self.plugin)],
            notification_listener_factories=[DummyNotificationListenerFactory(plugin=self.plugin)],
        )

    def tearDown(self):
        self.plugin.stop()

    def test_initialization(self):
        self.assertEqual(len(self.registry.mco_factories), 1)
        self.assertEqual(len(self.registry.data_source_factories), 1)
        self.assertEqual(len(self.registry.notification_listener_factories), 1)

    def test_lookup(self):
        mco_id = factory_id(self.plugin.id, "dummy_mco")
        parameter_id = mco_parameter_id(mco_id, "dummy_mco_parameter")
        self.assertEqual(self.registry.mco_factory_by_id(mco_id).id, mco_id)
        self.registry.mco_parameter_factory_by_id(mco_id, parameter_id)

        id = factory_id(self.plugin.id, "dummy_data_source")
        self.assertEqual(self.registry.data_source_factory_by_id(id).id, id)

        id = factory_id(self.plugin.id, "dummy_notification_listener")
        self.assertEqual(
            self.registry.notification_listener_factory_by_id(id).id,
            id)

        with self.assertRaises(KeyError):
            self.registry.mco_factory_by_id(
                factory_id(self.plugin.id, "foo"))

        with self.assertRaises(KeyError):
            self.registry.mco_parameter_factory_by_id(
                mco_id,
                mco_parameter_id(mco_id, "foo")
            )

        with self.assertRaises(KeyError):
            self.registry.data_source_factory_by_id(
                factory_id(self.plugin.id, "foo")
            )

        with self.assertRaises(KeyError):
            self.registry.data_source_factory_by_id(
                factory_id(self.plugin.id, "foo")
            )

        with self.assertRaises(KeyError):
            self.registry.notification_listener_factory_by_id(
                factory_id(self.plugin.id, "foo")
            )
