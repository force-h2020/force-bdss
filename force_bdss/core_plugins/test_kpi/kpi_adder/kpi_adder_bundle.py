from traits.api import provides, HasStrictTraits, String

from force_bdss.api import bundle_id
from force_bdss.api import IKPICalculatorBundle

from .kpi_adder_model import KPIAdderModel
from .kpi_adder_calculator import KPIAdderCalculator


@provides(IKPICalculatorBundle)
class KPIAdderBundle(HasStrictTraits):
    id = String(bundle_id("enthought", "kpi_adder"))

    def create_model(self, model_data=None):
        if model_data is None:
            return KPIAdderModel()
        else:
            return KPIAdderModel.from_json(model_data)

    def create_data_source(self, application, model):
        return KPIAdderCalculator(self, application, model)
