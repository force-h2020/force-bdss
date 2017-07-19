from force_bdss.base_extension_plugin import BaseExtensionPlugin

from .kpi_adder.kpi_adder_bundle import KPIAdderBundle


class TestKPICalculatorPlugin(BaseExtensionPlugin):
    def _kpi_calculator_bundles_default(self):
        return [KPIAdderBundle()]
