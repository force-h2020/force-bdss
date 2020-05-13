#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Any

from force_bdss.core.factory_registry import FactoryRegistry
from force_bdss.tests.dummy_classes.data_source import DummyDataSourceFactory
from force_bdss.tests.dummy_classes.extension_plugin import \
    DummyExtensionPlugin
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory
from force_bdss.tests.dummy_classes.notification_listener import \
    DummyNotificationListenerFactory
from force_bdss.ui_hooks.tests.test_base_ui_hooks_factory import \
    DummyUIHooksFactory


class DummyFactoryRegistry(FactoryRegistry):

    plugin = Any()

    def _plugin_default(self):
        return DummyExtensionPlugin()

    def _mco_factories_default(self):
        return [DummyMCOFactory(self.plugin)]

    def _data_source_factories_default(self):
        return [DummyDataSourceFactory(self.plugin)]

    def _notification_listener_factories_default(self):
        return [DummyNotificationListenerFactory(self.plugin)]

    def _ui_hooks_factories_default(self):
        return [DummyUIHooksFactory(self.plugin)]
