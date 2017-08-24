from traits.api import List

from force_bdss.factory_registry_plugin import FactoryRegistryPlugin

from .kpi_calculator import ProbeKPICalculatorFactory


class ProbeFactoryRegistryPlugin(FactoryRegistryPlugin):
    mco_factories = List()
    kpi_calculator_factories = List()
    data_source_factories = List()
    notification_listener_factories = List()

    def _kpi_calculator_factories_default(self):
        return ProbeKPICalculatorFactory(self)
