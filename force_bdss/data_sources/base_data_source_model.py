from traits.api import ABCHasStrictTraits, Instance, List, String, Event

from force_bdss.core.input_slot_map import InputSlotMap
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
    output_slot_names = List(String(), visible=False)

    #: This event claims that a change in the model influences the slots
    #: (either input or output). It must be triggered every time a specific
    #: option in your model implies a change in the slots. The UI will detect
    #: this and adapt the visual entries.
    changes_slots = Event()

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        super(BaseDataSourceModel, self).__init__(*args, **kwargs)

    def __getstate__(self):
        state = super(BaseDataSourceModel, self).__getstate__()
        state["input_slot_maps"] = [
            x.__getstate__() for x in self.input_slot_maps
        ]
        return state
