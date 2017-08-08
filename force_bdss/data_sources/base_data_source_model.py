from traits.api import ABCHasStrictTraits, Instance, List

from force_bdss.core.input_slot_map import InputSlotMap
from force_bdss.local_traits import Identifier
from .i_data_source_factory import IDataSourceFactory


class BaseDataSourceModel(ABCHasStrictTraits):
    """Base class for the factory specific DataSource models.
    This model will also provide, through traits/traitsui magic the View
    that will appear in the workflow manager UI.

    In your factory definition, your factory-specific model must reimplement
    this class.
    """
    #: A reference to the creating factory, so that we can
    #: retrieve it as the originating factory.
    factory = Instance(IDataSourceFactory, visible=False, transient=True)

    #: Specifies binding between input slots and source for that value.
    #: Each InputSlotMap instance specifies this information for each of the
    #: slots.
    input_slot_maps = List(Instance(InputSlotMap), visible=False)

    #: Allows to assign names to the output slots, so that they can be
    #: referenced somewhere else (e.g. the KPICalculators).
    #: If the name is the empty string, it means that the user is not
    #: interested in preserving the information, and should therefore be
    #: discarded and not propagated further.
    output_slot_names = List(Identifier(), visible=False)

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        super(BaseDataSourceModel, self).__init__(*args, **kwargs)

    def __getstate__(self):
        state = super(BaseDataSourceModel, self).__getstate__()
        state["input_slot_maps"] = [
            x.__getstate__() for x in self.input_slot_maps
        ]
        return state
