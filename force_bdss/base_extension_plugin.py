from envisage.plugin import Plugin
from traits.trait_types import List

from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle
from force_bdss.kpi.i_kpi_calculator_bundle import IKPICalculatorBundle
from force_bdss.mco.i_multi_criteria_optimizer_bundle import \
    IMultiCriteriaOptimizerBundle


class BaseExtensionPlugin(Plugin):
    mco_bundles = List(
        IMultiCriteriaOptimizerBundle,
        contributes_to='force.bdss.mco.bundles'
    )

    #: A list of the available Data Sources.
    #: It will be populated by plugins.
    data_source_bundles = List(
        IDataSourceBundle,
        contributes_to='force.bdss.data_sources.bundles')

    kpi_calculator_bundles = List(
        IKPICalculatorBundle,
        contributes_to='force.bdss.kpi_calculators.bundles'
    )
