from envisage.extension_point import ExtensionPoint
from envisage.plugin import Plugin
from traits.api import List

from force_bdss.ids import ExtensionPointID
from force_bdss.notification_listeners.i_notification_listener_bundle import \
    INotificationListenerBundle
from .data_sources.i_data_source_bundle import (
    IDataSourceBundle)
from .kpi.i_kpi_calculator_bundle import IKPICalculatorBundle
from .mco.i_mco_bundle import (
    IMCOBundle
)


BUNDLE_REGISTRY_PLUGIN_ID = "force.bdss.plugins.bundle_registry"


class BundleRegistryPlugin(Plugin):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """
    id = BUNDLE_REGISTRY_PLUGIN_ID

    # Note: we are forced to declare these extensions points here instead
    # of the application object, and this is why we have to use this plugin.
    # It is a workaround to an envisage bug that does not find the extension
    # points if declared on the application.

    #: A List of the available Multi Criteria Optimizers.
    #: This will be populated by MCO plugins.
    mco_bundles = ExtensionPoint(
        List(IMCOBundle),
        id=ExtensionPointID.MCO_BUNDLES)

    #: A list of the available Data Sources.
    #: It will be populated by plugins.
    data_source_bundles = ExtensionPoint(
        List(IDataSourceBundle),
        id=ExtensionPointID.DATA_SOURCE_BUNDLES)

    #: A list of the available Key Performance Indicator calculators.
    #: It will be populated by plugins.
    kpi_calculator_bundles = ExtensionPoint(
        List(IKPICalculatorBundle),
        id=ExtensionPointID.KPI_CALCULATOR_BUNDLES)

    notification_listener_bundles = ExtensionPoint(
        List(INotificationListenerBundle),
        id=ExtensionPointID.NOTIFICATION_LISTENER_BUNDLE
    )

    def data_source_bundle_by_id(self, id):
        """Finds a given data source bundle by means of its id.
        The ID is as obtained by the function bundle_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the bundle_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for ds in self.data_source_bundles:
            if ds.id == id:
                return ds

        raise KeyError(
            "Requested data source {} but don't know how "
            "to find it.".format(id))

    def kpi_calculator_bundle_by_id(self, id):
        """Finds a given kpi bundle by means of its id.
        The ID is as obtained by the function bundle_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the bundle_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for kpic in self.kpi_calculator_bundles:
            if kpic.id == id:
                return kpic

        raise KeyError(
            "Requested kpi calculator {} but don't know how "
            "to find it.".format(id))

    def mco_bundle_by_id(self, id):
        """Finds a given Multi Criteria Optimizer (MCO) bundle by means of
        its id. The ID is as obtained by the function bundle_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the bundle_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for mco in self.mco_bundles:
            if mco.id == id:
                return mco

        raise KeyError("Requested MCO {} but don't know how "
                       "to find it.".format(id))

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
        mco_bundle = self.mco_bundle_by_id(mco_id)

        for factory in mco_bundle.parameter_factories():
            if factory.id == parameter_id:
                return factory

        raise KeyError("Requested MCO parameter {}:{} but don't know"
                       " how to find it.".format(mco_id, parameter_id))

    def notification_listener_bundle_by_id(self, id):
        """Finds a given notification listener by means of its id.
        The ID is as obtained by the function bundle_id() in the
        plugin api.

        Parameters
        ----------
        id: str
            The identifier returned by the bundle_id() function.

        Raises
        ------
        KeyError: if the entry is not found.
        """
        for nl in self.notification_listener_bundles:
            if nl.id == id:
                return nl

        raise KeyError(
            "Requested notification listener {} but don't know how "
            "to find it.".format(id))
