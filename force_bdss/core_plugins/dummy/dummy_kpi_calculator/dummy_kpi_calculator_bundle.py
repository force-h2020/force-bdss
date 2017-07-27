from traits.api import String
from force_bdss.api import bundle_id, BaseKPICalculatorBundle
from .dummy_kpi_calculator import DummyKPICalculator
from .dummy_kpi_calculator_model import DummyKPICalculatorModel


class DummyKPICalculatorBundle(BaseKPICalculatorBundle):
    id = String(bundle_id("enthought", "dummy_kpi_calculator"))

    name = String("Dummy KPI")

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}

        return DummyKPICalculatorModel(self, **model_data)

    def create_kpi_calculator(self):
        return DummyKPICalculator(self)
