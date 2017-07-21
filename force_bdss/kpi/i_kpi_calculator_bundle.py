from traits.api import Interface, String


class IKPICalculatorBundle(Interface):
    """Envisage required interface for the BaseKPICalculatorBundle.
    You should not need to use this directly."""
    id = String()

    name = String()

    def create_kpi_calculator(self, application, model):
        pass

    def create_model(self, model_data=None):
        pass
