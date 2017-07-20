import abc
from traits.api import ABCHasStrictTraits, provides, String

from .i_kpi_calculator_bundle import IKPICalculatorBundle


@provides(IKPICalculatorBundle)
class BaseKPICalculatorBundle(ABCHasStrictTraits):
    id = String()

    name = String()

    @abc.abstractmethod
    def create_kpi_calculator(self, application, model):
        pass

    @abc.abstractmethod
    def create_model(self, model_data=None):
        pass
