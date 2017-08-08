from traits.api import String

from force_bdss.api import factory_id, BaseKPICalculatorFactory

from .kpi_adder_model import KPIAdderModel
from .kpi_adder_calculator import KPIAdderCalculator


class KPIAdderFactory(BaseKPICalculatorFactory):
    id = String(factory_id("enthought", "kpi_adder"))

    name = String("KPI Adder")

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}

        return KPIAdderModel(self, **model_data)

    def create_kpi_calculator(self):
        return KPIAdderCalculator(self)
