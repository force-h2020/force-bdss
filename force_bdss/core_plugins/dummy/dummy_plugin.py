from force_bdss.api import BaseExtensionPlugin, plugin_id
from force_bdss.core_plugins.dummy.dummy_notification_listener\
    .dummy_notification_listener_factory import \
    DummyNotificationListenerFactory
from .csv_extractor.csv_extractor_factory import CSVExtractorFactory
from .kpi_adder.kpi_adder_factory import KPIAdderFactory
from .dummy_dakota.dakota_factory import DummyDakotaFactory
from .dummy_data_source.dummy_data_source_factory import DummyDataSourceFactory
from .dummy_kpi_calculator.dummy_kpi_calculator_factory import (
    DummyKPICalculatorFactory
)


class DummyPlugin(BaseExtensionPlugin):
    id = plugin_id("enthought", "DummyPlugin")

    def _data_source_factories_default(self):
        return [DummyDataSourceFactory(self),
                CSVExtractorFactory(self)]

    def _mco_factories_default(self):
        return [DummyDakotaFactory(self)]

    def _kpi_calculator_factories_default(self):
        return [DummyKPICalculatorFactory(self),
                KPIAdderFactory(self)]

    def _notification_listener_factories_default(self):
        return [DummyNotificationListenerFactory(self)]
