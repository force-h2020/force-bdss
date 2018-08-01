from force_bdss.base_extension_plugin import BaseExtensionPlugin
from force_bdss.ids import plugin_id
from force_bdss.tests.dummy_classes.data_source import DummyDataSourceFactory
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory
from force_bdss.tests.dummy_classes.notification_listener import \
    DummyNotificationListenerFactory


class DummyExtensionPlugin(BaseExtensionPlugin):
    id = plugin_id("enthought", "test", 0)

    def get_name(self):
        return "Dummy extension"

    def get_description(self):
        return "Dummy description"

    def get_version(self):
        return 0

    def get_factory_classes(self):
        return [
            DummyMCOFactory,
            DummyDataSourceFactory,
            DummyNotificationListenerFactory
        ]
