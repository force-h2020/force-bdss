from traits.api import provides, HasStrictTraits
from traits.trait_types import String

from force_bdss.kpi.i_kpi_calculator_bundle import IKPICalculatorBundle

from .kpi_adder_model import KPIAdderModel
from .kpi_adder_calculator import KPIAdderCalculator


@provides(IKPICalculatorBundle)
class KPIAdderBundle(HasStrictTraits):
    name = String("kpi_adder")

    def create_model(self, model_data):
        return KPIAdderModel.from_json(model_data)

    def create_data_source(self, application, model):
        return KPIAdderCalculator(self, application, model)
