from force_bdss.api import BaseExtensionPlugin

from .kpi_adder.kpi_adder_bundle import KPIAdderBundle


class TestKPICalculatorPlugin(BaseExtensionPlugin):
    def _kpi_calculator_bundles_default(self):
        return [KPIAdderBundle()]
