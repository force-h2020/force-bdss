from envisage.plugin import Plugin
from traits.trait_types import List

from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle
from force_bdss.kpi.i_kpi_calculator_bundle import IKPICalculatorBundle
from force_bdss.mco.i_multi_criteria_optimizer_bundle import \
    IMultiCriteriaOptimizerBundle


class BaseExtensionPlugin(Plugin):
    """Base class for extension plugins, that is, plugins that are
    provided by external contributors.

    It provides a set of slots to be populated that end up contributing
    to the application extension points. To use the class, simply inherit it
    in your plugin, and then define the trait default initializer for the
    specific trait you want to populate. For example::

        class MyPlugin(BaseExtensionPlugin):
            def _data_source_bundles(self):
                return [MyDataSourceBundle1(),
                        MyDataSourceBundle2()]
    """

    #: A list of available Multi Criteria Optimizers this plugin exports.
    mco_bundles = List(
        IMultiCriteriaOptimizerBundle,
        contributes_to='force.bdss.mco.bundles'
    )

    #: A list of the available Data Sources this plugin exports.
    data_source_bundles = List(
        IDataSourceBundle,
        contributes_to='force.bdss.data_sources.bundles'
    )

    #: A list of the available KPI calculators this plugin exports.
    kpi_calculator_bundles = List(
        IKPICalculatorBundle,
        contributes_to='force.bdss.kpi_calculators.bundles'
    )
