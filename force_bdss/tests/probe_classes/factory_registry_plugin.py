from traits.api import List, HasStrictTraits, provides

from force_bdss.factory_registry_plugin import IFactoryRegistryPlugin

from .mco import ProbeMCOFactory
from .kpi_calculator import ProbeKPICalculatorFactory
from .data_source import ProbeDataSourceFactory
from .notification_listener import ProbeNotificationListenerFactory
from .ui_hooks import ProbeUIHooksFactory


@provides(IFactoryRegistryPlugin)
class ProbeFactoryRegistryPlugin(HasStrictTraits):
    mco_factories = List()
    kpi_calculator_factories = List()
    data_source_factories = List()
    notification_listener_factories = List()
    ui_hooks_factories = List()

    def _mco_factories_default(self):
        return [ProbeMCOFactory(None)]

    def _kpi_calculator_factories_default(self):
        return [ProbeKPICalculatorFactory(None)]

    def _data_source_factories_default(self):
        return [ProbeDataSourceFactory(None)]

    def _notification_listener_factories_default(self):
        return [ProbeNotificationListenerFactory(None)]

    def _ui_hooks_factories_default(self):
        return [ProbeUIHooksFactory(None)]

    def data_source_factory_by_id(self, id):
        for ds in self.data_source_factories:
            if ds.id == id:
                return ds

        raise KeyError(id)

    def kpi_calculator_factory_by_id(self, id):
        for kpic in self.kpi_calculator_factories:
            if kpic.id == id:
                return kpic

        raise KeyError(id)

    def mco_factory_by_id(self, id):
        for mco in self.mco_factories:
            if mco.id == id:
                return mco

        raise KeyError(id)

    def mco_parameter_factory_by_id(self, mco_id, parameter_id):
        mco_factory = self.mco_factory_by_id(mco_id)

        for factory in mco_factory.parameter_factories():
            if factory.id == parameter_id:
                return factory

        raise KeyError(parameter_id)

    def notification_listener_factory_by_id(self, id):
        for nl in self.notification_listener_factories:
            if nl.id == id:
                return nl

        raise KeyError(id)

