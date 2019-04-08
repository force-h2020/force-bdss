from traits.api import HasStrictTraits, List, provides, Any

from force_bdss.core.i_factory_registry import IFactoryRegistry
from force_bdss.tests.dummy_classes.data_source import DummyDataSourceFactory
from force_bdss.tests.dummy_classes.extension_plugin import \
    DummyExtensionPlugin
from force_bdss.tests.dummy_classes.mco import DummyMCOFactory
from force_bdss.tests.dummy_classes.notification_listener import \
    DummyNotificationListenerFactory
from force_bdss.ui_hooks.tests.test_base_ui_hooks_factory import \
    DummyUIHooksFactory


@provides(IFactoryRegistry)
class DummyFactoryRegistryPlugin(HasStrictTraits):
    mco_factories = List()
    data_source_factories = List()
    notification_listener_factories = List()
    ui_hooks_factories = List()

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

    def data_source_factory_by_id(self, id):
        for ds in self.data_source_factories:
            if ds.id == id:
                return ds

        raise KeyError(id)

    def mco_factory_by_id(self, id):
        for mco in self.mco_factories:
            if mco.id == id:
                return mco

        raise KeyError(id)

    def mco_parameter_factory_by_id(self, mco_id, parameter_id):
        mco_factory = self.mco_factory_by_id(mco_id)

        for factory in mco_factory.parameter_factories:
            if factory.id == parameter_id:
                return factory

        raise KeyError(parameter_id)

    def notification_listener_factory_by_id(self, id):
        for nl in self.notification_listener_factories:
            if nl.id == id:
                return nl

        raise KeyError(id)

    #: Service offers provided by this plugin.
    service_offers = List()

    def _create_factory_registry(self):
        return self

    def _service_offers_default(self):
        factory_registry_offer = ServiceOffer(
            protocol=IFactoryRegistry,
            factory=self._create_factory_registry,
        )
        return [factory_registry_offer]
