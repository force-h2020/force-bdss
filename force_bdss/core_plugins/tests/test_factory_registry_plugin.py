#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest
import warnings

from force_bdss.ids import factory_id, mco_parameter_id
from force_bdss.tests.dummy_classes.extension_plugin import \
    DummyExtensionPlugin

from envisage.application import Application

from force_bdss.core_plugins.factory_registry_plugin import \
    FactoryRegistryPlugin


class TestFactoryRegistry(unittest.TestCase):
    def setUp(self):
        self.plugin = FactoryRegistryPlugin()
        self.app = Application([self.plugin])
        self.app.start()
        self.app.stop()

    def test_initialization(self):
        self.assertEqual(self.plugin.mco_factories, [])
        self.assertEqual(self.plugin.data_source_factories, [])


class TestFactoryRegistryWithContent(unittest.TestCase):
    def setUp(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.registry = FactoryRegistryPlugin()
            self.plugin = DummyExtensionPlugin()
            self.app = Application([self.registry, self.plugin])
            self.app.start()
            self.app.stop()

    def test_initialization(self):
        self.assertEqual(len(self.registry.mco_factories), 1)
        self.assertEqual(len(self.registry.data_source_factories), 1)

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
