from force_bdss.base_extension_plugin import BaseExtensionPlugin
from force_bdss.ids import plugin_id
from force_bdss.tests.probe_classes.data_source import ProbeDataSourceFactory
from force_bdss.tests.probe_classes.mco import ProbeMCOFactory
from force_bdss.tests.probe_classes.notification_listener import \
    ProbeNotificationListenerFactory
from force_bdss.tests.probe_classes.ui_hooks import ProbeUIHooksFactory


class ProbeExtensionPlugin(BaseExtensionPlugin):
    id = plugin_id("enthought", "test")
    factory_classes = [
        ProbeDataSourceFactory,
        ProbeMCOFactory,
        ProbeNotificationListenerFactory,
        ProbeUIHooksFactory,
    ]
