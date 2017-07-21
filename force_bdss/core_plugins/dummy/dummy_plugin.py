from force_bdss.api import BaseExtensionPlugin
from .dummy_dakota.dakota_bundle import DummyDakotaBundle
from .dummy_data_source.dummy_data_source_bundle import DummyDataSourceBundle
from .dummy_kpi_calculator.dummy_kpi_calculator_bundle import (
    DummyKPICalculatorBundle
)


class DummyPlugin(BaseExtensionPlugin):
    def _data_source_bundles_default(self):
        return [DummyDataSourceBundle()]

    def _mco_bundles_default(self):
        return [DummyDakotaBundle()]

    def _kpi_calculator_bundles_default(self):
        return [DummyKPICalculatorBundle()]
