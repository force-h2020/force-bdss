from envisage.plugin import Plugin
from traits.api import List

from force_bdss.kpi.i_kpi_calculator_bundle import (
    IKPICalculatorBundle)

from .kpi_adder.kpi_adder_bundle import KPIAdderBundle


class TestKPICalculatorPlugin(Plugin):
    id = "force.bdss.plugins.enthought.test_kpi_calculator_plugin"

    kpi_calculators = List(
        IKPICalculatorBundle,
        contributes_to='force.bdss.kpi_calculators.bundles'
    )

    def _kpi_calculators_default(self):
        return [KPIAdderBundle()]
