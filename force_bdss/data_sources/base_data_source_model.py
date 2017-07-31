from traits.api import ABCHasStrictTraits, Instance, List, String

from ..core.input_slot_map import InputSlotMap
from .i_data_source_bundle import IDataSourceBundle


class BaseDataSourceModel(ABCHasStrictTraits):
    """Base class for the bundle specific DataSource models.
    This model will also provide, through traits/traitsui magic the View
    that will appear in the workflow manager UI.

    In your bundle definition, your bundle-specific model must reimplement
    this class.
    """
    #: A reference to the creating bundle, so that we can
    #: retrieve it as the originating factory.
    bundle = Instance(IDataSourceBundle, visible=False, transient=True)

    #: Specifies binding between input slots and source for that value.
    #: Each InputSlotMap instance specifies this information for each of the
    #: slots.
    input_slot_maps = List(Instance(InputSlotMap))

    #: Allows to assign names to the output slots, so that they can be
    #: referenced somewhere else (e.g. the KPICalculators).
    output_slot_names = List(String())

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseDataSourceModel, self).__init__(*args, **kwargs)
