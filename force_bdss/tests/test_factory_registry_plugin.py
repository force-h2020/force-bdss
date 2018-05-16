import unittest
import warnings

from force_bdss.base_extension_plugin import (
    BaseExtensionPlugin)
from force_bdss.data_sources.base_data_source_factory import \
    BaseDataSourceFactory
from force_bdss.ids import factory_id, mco_parameter_id
from force_bdss.mco.base_mco_factory import BaseMCOFactory
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory
from force_bdss.notification_listeners.base_notification_listener_factory \
    import \
    BaseNotificationListenerFactory
from force_bdss.notification_listeners.i_notification_listener_factory import \
    INotificationListenerFactory

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.application import Application

from force_bdss.factory_registry_plugin import FactoryRegistryPlugin
from force_bdss.data_sources.i_data_source_factory import IDataSourceFactory
from force_bdss.mco.i_mco_factory import IMCOFactory


class TestFactoryRegistry(unittest.TestCase):
    def setUp(self):
        self.plugin = FactoryRegistryPlugin()
        self.app = Application([self.plugin])
        self.app.start()
        self.app.stop()

    def test_initialization(self):
        self.assertEqual(self.plugin.mco_factories, [])
        self.assertEqual(self.plugin.data_source_factories, [])


class MCOFactory(BaseMCOFactory):
    id = factory_id("enthought", "mco1")

    def parameter_factories(self):
        return [
            mock.Mock(
                spec=BaseMCOParameterFactory,
                id=mco_parameter_id("enthought", "mco1", "ranged")
            )
        ]


class DataSourceFactory1(BaseDataSourceFactory):
    id = factory_id("enthought", "ds1")


class DataSourceFactory2(BaseDataSourceFactory):
    id = factory_id("enthought", "ds2")


class NotificationListenerFactory(BaseNotificationListenerFactory):
    id = factory_id("enthought", "nl1")


class MySuperPlugin(BaseExtensionPlugin):
    def get_producer(self):
        return "enthought"

    def get_identifier(self):
        return "test"

    def get_factory_classes(self):
        return [
            MCOFactory,
            DataSourceFactory1,
            DataSourceFactory2,
            NotificationListenerFactory
        ]


class TestFactoryRegistryWithContent(unittest.TestCase):
    def setUp(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.plugin = FactoryRegistryPlugin()
            self.app = Application([self.plugin, MySuperPlugin()])
            self.app.start()
            self.app.stop()

    def test_initialization(self):
        self.assertEqual(len(self.plugin.mco_factories), 1)
        self.assertEqual(len(self.plugin.data_source_factories), 2)

    def test_lookup(self):
        mco_id = factory_id("enthought", "mco1")
        parameter_id = mco_parameter_id("enthought", "mco1", "ranged")
        self.assertEqual(self.plugin.mco_factory_by_id(mco_id).id, mco_id)
        self.plugin.mco_parameter_factory_by_id(mco_id, parameter_id)

        for entry in ["ds1", "ds2"]:
            id = factory_id("enthought", entry)
            self.assertEqual(self.plugin.data_source_factory_by_id(id).id, id)

        for entry in ["nl1"]:
            id = factory_id("enthought", entry)
            self.assertEqual(
                self.plugin.notification_listener_factory_by_id(id).id,
                id)

        with self.assertRaises(KeyError):
            self.plugin.mco_factory_by_id(
                factory_id("enthought", "foo"))

        with self.assertRaises(KeyError):
            self.plugin.mco_parameter_factory_by_id(
                mco_id,
                mco_parameter_id("enthought", "mco1", "foo")
            )

        with self.assertRaises(KeyError):
            self.plugin.data_source_factory_by_id(
                factory_id("enthought", "foo")
            )

        with self.assertRaises(KeyError):
            self.plugin.data_source_factory_by_id(
                factory_id("enthought", "foo")
            )

        with self.assertRaises(KeyError):
            self.plugin.notification_listener_factory_by_id(
                factory_id("enthought", "foo")
            )


if __name__ == '__main__':
    unittest.main()
