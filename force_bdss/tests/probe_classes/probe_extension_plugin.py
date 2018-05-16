from force_bdss.base_extension_plugin import BaseExtensionPlugin
from force_bdss.tests.probe_classes.data_source import ProbeDataSourceFactory
from force_bdss.tests.probe_classes.mco import ProbeMCOFactory
from force_bdss.tests.probe_classes.notification_listener import \
    ProbeNotificationListenerFactory
from force_bdss.tests.probe_classes.ui_hooks import ProbeUIHooksFactory


class ProbeExtensionPlugin(BaseExtensionPlugin):
    def get_producer(self):
        return "enthought"

    def get_identifier(self):
        return "test"

    def get_factory_classes(self):
        return [
            ProbeDataSourceFactory,
            ProbeMCOFactory,
            ProbeNotificationListenerFactory,
            ProbeUIHooksFactory,
        ]
