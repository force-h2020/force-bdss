from traits.api import Interface, String, Instance
from envisage.plugin import Plugin

from force_bdss.kpi.base_kpi_calculator import BaseKPICalculator
from force_bdss.kpi.base_kpi_calculator_model import BaseKPICalculatorModel


class IKPICalculatorFactory(Interface):
    """Envisage required interface for the BaseKPICalculatorFactory.
    You should not need to use this directly.

    Refer to the BaseKPICalculatorFactory for documentation.
    """
    id = String()

    name = String()

    kpi_calculator_class = Instance(BaseKPICalculator)

    model_class = Instance(BaseKPICalculatorModel)

    plugin = Instance(Plugin)

    def create_kpi_calculator(self):
        """"""

    def create_model(self, model_data=None):
        """"""
