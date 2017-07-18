from envisage.extension_point import ExtensionPoint
from envisage.plugin import Plugin
from traits.api import List

from force_bdss.data_sources.i_data_source_bundle import (
    IDataSourceBundle)
from force_bdss.kpi.i_kpi_calculator_bundle import IKPICalculatorBundle
from force_bdss.mco.i_multi_criteria_optimizer_bundle import (
    IMultiCriteriaOptimizerBundle)


class BaseCoreDriver(Plugin):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    # Note: we are forced to declare these extensions points here instead
    # of the application object, and this is why we have to use this plugin.
    # It is a workaround to an envisage bug that does not find the extension
    # points if declared on the application.

    #: A List of the available Multi Criteria Optimizers.
    #: This will be populated by MCO plugins.
    mco_bundles = ExtensionPoint(
        List(IMultiCriteriaOptimizerBundle),
        id='force.bdss.mco.bundles')

    #: A list of the available Data Sources.
    #: It will be populated by plugins.
    data_source_bundles = ExtensionPoint(
        List(IDataSourceBundle),
        id='force.bdss.data_sources.bundles')

    #: A list of the available Key Performance Indicator calculators.
    #: It will be populated by plugins.
    kpi_calculator_bundles = ExtensionPoint(
        List(IKPICalculatorBundle),
        id='force.bdss.kpi_calculators.bundles')

    def _data_source_bundle_by_name(self, name):
        for ds in self.data_source_bundles:
            if ds.name == name:
                return ds

        raise Exception("Requested data source {} but don't know "
                        "to find it.".format(name))

    def _kpi_calculator_bundle_by_name(self, name):
        for kpic in self.kpi_calculator_bundles:
            if kpic.name == name:
                return kpic

        raise Exception(
            "Requested kpi calculator {} but don't know "
            "to find it.".format(name))

    def _mco_bundle_by_name(self, name):
        for mco in self.mco_bundles:
            if mco.name == name:
                return mco

        raise Exception("Requested MCO {} but it's not available"
                        "to compute it.".format(name))
