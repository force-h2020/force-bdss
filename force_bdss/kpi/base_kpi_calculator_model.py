from traits.api import ABCHasStrictTraits, Instance

from .i_kpi_calculator_bundle import IKPICalculatorBundle


class BaseKPICalculatorModel(ABCHasStrictTraits):
    bundle = Instance(IKPICalculatorBundle, visible=False, transient=True)

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseKPICalculatorModel, self).__init__(*args, **kwargs)
