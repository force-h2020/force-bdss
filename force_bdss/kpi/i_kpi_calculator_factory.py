from traits.api import Interface, String, Instance
from envisage.plugin import Plugin


class IKPICalculatorFactory(Interface):
    """Envisage required interface for the BaseKPICalculatorFactory.
    You should not need to use this directly.

    Refer to the BaseKPICalculatorFactory for documentation.
    """
    id = String()

    name = String()

    plugin = Instance(Plugin)

    def create_kpi_calculator(self):
        """"""

    def create_model(self, model_data=None):
        """"""
