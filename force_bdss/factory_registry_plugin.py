from envisage.extension_point import ExtensionPoint
from envisage.plugin import Plugin
from traits.api import List

from force_bdss.ids import ExtensionPointID
from force_bdss.notification_listeners.i_notification_listener_factory import \
    INotificationListenerFactory
from .data_sources.i_data_source_factory import (
    IDataSourceFactory)
from .kpi.i_kpi_calculator_factory import IKPICalculatorFactory
from .mco.i_mco_factory import IMCOFactory
from .ui_hooks.i_ui_hooks_factory import IUIHooksFactory


FACTORY_REGISTRY_PLUGIN_ID = "force.bdss.plugins.factory_registry"


class FactoryRegistryPlugin(Plugin):
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

    #: A list of the available Key Performance Indicator calculators.
    #: It will be populated by plugins.
    kpi_calculator_factories = ExtensionPoint(
        List(IKPICalculatorFactory),
        id=ExtensionPointID.KPI_CALCULATOR_FACTORIES)

    #: Notification listeners are pluggable entities that will listen
    #: to MCO events and act accordingly.
    notification_listener_factories = ExtensionPoint(
        List(INotificationListenerFactory),
        id=ExtensionPointID.NOTIFICATION_LISTENER_FACTORIES
    )

    ui_hooks_factories = ExtensionPoint(
        List(IUIHooksFactory),
        id=ExtensionPointID.UI_HOOK_FACTORIES
    )

    def data_source_factory_by_id(self, id):
        """Finds a given data source factory by means of its id.
        The ID is as obtained by the function factory_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the factory_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for ds in self.data_source_factories:
            if ds.id == id:
                return ds

        raise KeyError(id)

    def kpi_calculator_factory_by_id(self, id):
        """Finds a given kpi factory by means of its id.
        The ID is as obtained by the function factory_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the factory_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for kpic in self.kpi_calculator_factories:
            if kpic.id == id:
                return kpic

        raise KeyError(id)

    def mco_factory_by_id(self, id):
        """Finds a given Multi Criteria Optimizer (MCO) factory by means of
        its id. The ID is as obtained by the function factory_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the factory_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for mco in self.mco_factories:
            if mco.id == id:
                return mco

        raise KeyError(id)

    def mco_parameter_factory_by_id(self, mco_id, parameter_id):
        """Retrieves the MCO parameter factory for a given MCO id and
        parameter id.

        Parameters
        ----------
        mco_id: str
            The MCO identifier string
        parameter_id: str
            the parameter identifier string

        Returns
        -------
        An instance of BaseMCOParameterFactory.

        Raises
        ------
        KeyError:
            if the entry is not found
        """
        mco_factory = self.mco_factory_by_id(mco_id)

        for factory in mco_factory.parameter_factories():
            if factory.id == parameter_id:
                return factory

        raise KeyError(parameter_id)

    def notification_listener_factory_by_id(self, id):
        """Finds a given notification listener by means of its id.
        The ID is as obtained by the function factory_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the factory_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for nl in self.notification_listener_factories:
            if nl.id == id:
                return nl

        raise KeyError(id)

    def ui_hook_factory_by_id(self, id):
        """Finds a given UI Hook factory by means of its id.
        The ID is as obtained by the function factory_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the factory_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for hook in self.ui_hooks_factories:
            if hook.id == id:
                return hook

        raise KeyError(id)

