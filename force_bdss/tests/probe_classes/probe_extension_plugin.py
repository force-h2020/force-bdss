from __future__ import unicode_literals
from force_bdss.base_extension_plugin import BaseExtensionPlugin
from force_bdss.ids import plugin_id
from force_bdss.tests.probe_classes.data_source import ProbeDataSourceFactory
from force_bdss.tests.probe_classes.mco import ProbeMCOFactory
from force_bdss.tests.probe_classes.notification_listener import \
    ProbeNotificationListenerFactory
from force_bdss.tests.probe_classes.ui_hooks import ProbeUIHooksFactory


class ProbeExtensionPlugin(BaseExtensionPlugin):
    id = plugin_id("enthought", "test", 0)

    def get_name(self):
        return "Probe extension"

    def get_description(self):
        return "A description"

    def get_version(self):
        return 0

    def get_factory_classes(self):
        return [
            ProbeDataSourceFactory,
            ProbeMCOFactory,
            ProbeNotificationListenerFactory,
            ProbeUIHooksFactory,
        ]
