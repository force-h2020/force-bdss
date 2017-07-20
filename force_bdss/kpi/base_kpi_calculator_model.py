from traits.api import ABCHasStrictTraits, Instance

from .i_kpi_calculator_bundle import IKPICalculatorBundle


class BaseKPICalculatorModel(ABCHasStrictTraits):
    """Base class for the bundle specific KPI calculator models.
    This model will also provide, through traits/traitsui magic the View
    that will appear in the workflow manager UI.

    In your bundle definition, your bundle-specific model must reimplement
    this class.
    """
    #: A reference to the creating bundle, so that we can
    #: retrieve it as the originating factory.
    bundle = Instance(IKPICalculatorBundle, visible=False, transient=True)

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseKPICalculatorModel, self).__init__(*args, **kwargs)
