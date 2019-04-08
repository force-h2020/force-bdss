from traits.api import List, HasStrictTraits, provides, Any

from force_bdss.core.factory_registry import FactoryRegistry
from force_bdss.core.i_factory_registry import IFactoryRegistry
from force_bdss.tests.probe_classes.probe_extension_plugin import \
    ProbeExtensionPlugin

from .mco import ProbeMCOFactory
from .data_source import ProbeDataSourceFactory
from .notification_listener import ProbeNotificationListenerFactory
from .ui_hooks import ProbeUIHooksFactory


@provides(IFactoryRegistry)
class ProbeFactoryRegistryPlugin(FactoryRegistry):
    service_offers = List()

    plugin = Any()

    def _plugin_default(self):
        return ProbeExtensionPlugin()

    def _mco_factories_default(self):
        return [ProbeMCOFactory(self.plugin)]

    def _data_source_factories_default(self):
        return [ProbeDataSourceFactory(self.plugin)]

    def _notification_listener_factories_default(self):
        return [ProbeNotificationListenerFactory(self.plugin)]

    def _ui_hooks_factories_default(self):
        return [ProbeUIHooksFactory(self.plugin)]

    def _create_factory_registry(self):
        return self

    def _service_offers_default(self):
        factory_registry_offer = ServiceOffer(
            protocol=IFactoryRegistry,
            factory=self._create_factory_registry,
        )
        return [factory_registry_offer]
