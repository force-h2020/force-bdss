from envisage.api import ExtensionPoint, Plugin, ServiceOffer
from traits.api import List, Instance, Interface, provides

from force_bdss.core.factory_registry import FactoryRegistry
from force_bdss.core.i_factory_registry import IFactoryRegistry
from force_bdss.ids import ExtensionPointID
from force_bdss.notification_listeners.i_notification_listener_factory import \
    INotificationListenerFactory
from .data_sources.i_data_source_factory import (
    IDataSourceFactory)
from .mco.i_mco_factory import IMCOFactory
from .ui_hooks.i_ui_hooks_factory import IUIHooksFactory


FACTORY_REGISTRY_PLUGIN_ID = "force.bdss.plugins.factory_registry"


@provides(IFactoryRegistry)
class FactoryRegistryPlugin(Plugin, FactoryRegistry):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """
    id = FACTORY_REGISTRY_PLUGIN_ID

    # Note: we are forced to declare these extensions points here instead
    # of the application object, and this is why we have to use this plugin.
    # It is a workaround to an envisage bug that does not find the extension
    # points if declared on the application.

    #: A List of the available Multi Criteria Optimizers.
    #: This will be populated by MCO plugins.
    mco_factories = ExtensionPoint(
        List(IMCOFactory),
        id=ExtensionPointID.MCO_FACTORIES)

    #: A list of the available Data Sources.
    #: It will be populated by plugins.
    data_source_factories = ExtensionPoint(
        List(IDataSourceFactory),
        id=ExtensionPointID.DATA_SOURCE_FACTORIES)

    #: Notification listeners are pluggable entities that will listen
    #: to MCO events and act accordingly.
    notification_listener_factories = ExtensionPoint(
        List(INotificationListenerFactory),
        id=ExtensionPointID.NOTIFICATION_LISTENER_FACTORIES
    )

    #: UI Hooks are pluggable entities holding methods that are called
    #: at specific moments in the UI application lifetime. They can be used
    #: to inject special behaviors at those moments.
    ui_hooks_factories = ExtensionPoint(
        List(IUIHooksFactory),
        id=ExtensionPointID.UI_HOOKS_FACTORIES
    )

    #: Service offers provided by this plugin.
    service_offers = List(Instance(ServiceOffer))

    def _create_factory_registry(self):
        return self

    def _service_offers_default(self):
        factory_registry_offer = ServiceOffer(
            protocol=IFactoryRegistry,
            factory=self._create_factory_registry,
        )
        return [factory_registry_offer]
