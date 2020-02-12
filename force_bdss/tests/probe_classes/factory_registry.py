from traits.api import Any

from force_bdss.core.factory_registry import FactoryRegistry
from force_bdss.tests.probe_classes.probe_extension_plugin import (
    ProbeExtensionPlugin,
)

from .mco import ProbeMCOFactory
from .data_source import ProbeDataSourceFactory
from .notification_listener import (
    ProbeNotificationListenerFactory,
    ProbeUINotificationListenerFactory,
)
from .ui_hooks import ProbeUIHooksFactory


class ProbeFactoryRegistry(FactoryRegistry):

    plugin = Any()

    def _plugin_default(self):
        return ProbeExtensionPlugin()

    def _mco_factories_default(self):
        return [ProbeMCOFactory(self.plugin)]

    def _data_source_factories_default(self):
        return [ProbeDataSourceFactory(self.plugin)]

    def _notification_listener_factories_default(self):
        return [
            ProbeNotificationListenerFactory(self.plugin),
            ProbeUINotificationListenerFactory(self.plugin),
        ]

    def _ui_hooks_factories_default(self):
        return [ProbeUIHooksFactory(self.plugin)]
