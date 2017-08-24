from traits.api import List

from force_bdss.factory_registry_plugin import FactoryRegistryPlugin

from .mco import ProbeMCOFactory
from .kpi_calculator import ProbeKPICalculatorFactory
from .data_source import ProbeDataSourceFactory


class ProbeFactoryRegistryPlugin(FactoryRegistryPlugin):
    mco_factories = List()
    kpi_calculator_factories = List()
    data_source_factories = List()
    notification_listener_factories = List()

    def _mco_factories_default(self):
        return [ProbeMCOFactory(self)]

    def _kpi_calculator_factories_default(self):
        return [ProbeKPICalculatorFactory(self)]

    def _data_source_factories_default(self):
        return [ProbeDataSourceFactory(self)]
