from traits.api import ABCHasStrictTraits, Instance, List, String

from ..core.input_slot_map import InputSlotMap
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

    #: Specifies binding between input slots and source for that value.
    #: Each InputSlotMap instance specifies this information for each of the
    #: slots.
    input_slot_maps = List(Instance(InputSlotMap))

    #: Allows to assign names to the output slots, so that they can be
    #: referenced somewhere else (e.g. the KPICalculators).
    output_slot_names = List(String())

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseKPICalculatorModel, self).__init__(*args, **kwargs)

    def __getstate__(self):
        state = super(BaseKPICalculatorModel, self).__getstate__()
        state["input_slot_maps"] = [
            x.__getstate__() for x in self.input_slot_maps
            ]
        return state
