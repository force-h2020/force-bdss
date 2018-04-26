from envisage.plugin import Plugin
from traits.trait_types import List

from .notification_listeners.i_notification_listener_factory import \
    INotificationListenerFactory
from .ids import ExtensionPointID
from .data_sources.i_data_source_factory import IDataSourceFactory
from .mco.i_mco_factory import IMCOFactory
from .ui_hooks.i_ui_hooks_factory import IUIHooksFactory


class BaseExtensionPlugin(Plugin):
    """Base class for extension plugins, that is, plugins that are
    provided by external contributors.

    It provides a set of slots to be populated that end up contributing
    to the application extension points. To use the class, simply inherit it
    in your plugin, and then define the trait default initializer for the
    specific trait you want to populate. For example::

        class MyPlugin(BaseExtensionPlugin):
            def _data_source_factories_default(self):
                return [MyDataSourceFactory1(),
                        MyDataSourceFactory2()]
    """

    #: A list of available Multi Criteria Optimizers this plugin exports.
    mco_factories = List(
        IMCOFactory,
        contributes_to=ExtensionPointID.MCO_FACTORIES
    )

    #: A list of the available Data Sources this plugin exports.
    data_source_factories = List(
        IDataSourceFactory,
        contributes_to=ExtensionPointID.DATA_SOURCE_FACTORIES
    )

    notification_listener_factories = List(
        INotificationListenerFactory,
        contributes_to=ExtensionPointID.NOTIFICATION_LISTENER_FACTORIES
    )

    ui_hooks_factories = List(
        IUIHooksFactory,
        contributes_to=ExtensionPointID.UI_HOOKS_FACTORIES
    )
