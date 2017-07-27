from force_bdss.api import BaseExtensionPlugin, plugin_id
from .csv_extractor.csv_extractor_bundle import CSVExtractorBundle
from .kpi_adder.kpi_adder_bundle import KPIAdderBundle
from .dummy_dakota.dakota_bundle import DummyDakotaBundle
from .dummy_data_source.dummy_data_source_bundle import DummyDataSourceBundle
from .dummy_kpi_calculator.dummy_kpi_calculator_bundle import (
    DummyKPICalculatorBundle
)


class DummyPlugin(BaseExtensionPlugin):
    id = plugin_id("enthought", "DummyPlugin")

    def _data_source_bundles_default(self):
        return [DummyDataSourceBundle(),
                CSVExtractorBundle()]

    def _mco_bundles_default(self):
        return [DummyDakotaBundle()]

    def _kpi_calculator_bundles_default(self):
        return [DummyKPICalculatorBundle(),
                KPIAdderBundle()]
