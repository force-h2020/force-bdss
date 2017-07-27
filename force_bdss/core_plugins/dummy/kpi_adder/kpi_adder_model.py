from traits.api import String

from force_bdss.api import BaseKPICalculatorModel


class KPIAdderModel(BaseKPICalculatorModel):
    cuba_type_in = String()
    cuba_type_out = String()
