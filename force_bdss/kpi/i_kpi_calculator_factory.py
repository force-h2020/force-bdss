from traits.api import Interface, String, Instance, Type
from envisage.plugin import Plugin


class IKPICalculatorFactory(Interface):
    """Envisage required interface for the BaseKPICalculatorFactory.
    You should not need to use this directly.

    Refer to the BaseKPICalculatorFactory for documentation.
    """
    id = String()

    name = String()

    kpi_calculator_class = Type(
        "force_bdss.kpi.base_kpi_calculator.BaseKPICalculator"
    )

    model_class = Type(
        "force_bdss.kpi.base_kpi_calculator_model.BaseKPICalculatorModel"
    )

    plugin = Instance(Plugin)

    def create_kpi_calculator(self):
        """"""

    def create_model(self, model_data=None):
        """"""
