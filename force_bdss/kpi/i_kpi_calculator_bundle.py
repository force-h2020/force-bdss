from traits.api import Interface, String, Instance
from envisage.plugin import Plugin


class IKPICalculatorBundle(Interface):
    """Envisage required interface for the BaseKPICalculatorBundle.
    You should not need to use this directly.

    Refer to the BaseKPICalculatorBundle for documentation.
    """
    id = String()

    name = String()

    plugin = Instance(Plugin)

    def create_kpi_calculator(self):
        pass

    def create_model(self, model_data=None):
        pass
