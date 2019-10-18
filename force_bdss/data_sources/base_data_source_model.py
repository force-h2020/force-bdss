from logging import getLogger

from traits.api import (
    Instance, List, Event, on_trait_change
)

from force_bdss.core.base_model import BaseModel
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.core.verifier import VerifierError
from force_bdss.data_sources.i_data_source_factory import IDataSourceFactory
from force_bdss.io.workflow_writer import pop_dunder_recursive

from .data_source_utilities import (
    merge_lists_with_check, merge_lists,
    retain_list
)

logger = getLogger(__name__)


class BaseDataSourceModel(BaseModel):
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
    input_slot_info = List(Instance(InputSlotInfo), visible=False)

    #: Allows to assign names and KPI status to the output slots, so that
    #: they can be referenced somewhere else (e.g. another layer's
    #: DataSources).
    #: If the name is the empty string, it means that the user is not
    #: interested in preserving the information, and should therefore be
    #: discarded and not propagated further.
    output_slot_info = List(Instance(OutputSlotInfo), visible=False)

    #: This event claims that a change in the model influences the slots
    #: (either input or output). It must be triggered every time a specific
    #: option in your model implies a change in the slots. The UI will detect
    #: this and adapt the visual entries.
    changes_slots = Event()

    def __init__(self, factory=None, *args, **kwargs):
        super(BaseDataSourceModel, self).__init__(factory, *args, **kwargs)
        # If either input_slot_info or output_slot_info have been passed in
        # as arguments, perform extra checks before assigning to make sure
        # they will be accepted by the BaseDataSource associated with factory
        self._assign_slot_info()

    # -------------------
    #      Listeners
    # -------------------

    @on_trait_change("+changes_slots")
    def _trigger_changes_slots(self, obj, name, new):
        changes_slots = self.traits()[name].changes_slots

        if changes_slots:
            self.changes_slots = True

    @on_trait_change('changes_slots')
    def _update_slot_info(self):
        """This method is designed to be performed upon a `change_slots`
        event to obtain the new format for input_slot_info
        and output_slot_info lists. It obtains the new input_slot_info
        and output_slot_info defaults, and updates the existing
        attributes with any format changes.

        A change_slots event can indicate 2 outcomes:
        1. Changes to the number of input and output Slot objects
        returned by the corresponding BaseDataSource
        2. Changes to attributes on each Slot object returned by the
        corresponding BaseDataSource

        In the first instance, we would like to retain any InputSlotInfo
        or OutputSlotInfo elements referring to variables that have
        been defined before. These are identified as having matching
        `type` and `description` attributes with an element in the
        new default slot lists.

        In the second instance, expect each element on the existing
        input_slot_info or output_slot_info lists to refer to the
        corresponding element on the new default lists returned by
        the _return_slots method. Therefore we simply update any
        attribute `type` and `description` values.
        """
        # Get new slots, caused by change_slots event
        for attr_name, slot_info in self._slot_info_generator():
            attr = getattr(self, attr_name)

            if len(slot_info) == len(attr):
                # If changes_slots event has not altered the length of
                # each list attribute, update each element with any
                # changed 'type' and 'description' values
                merge_lists(slot_info, attr, ['type', 'description'])
            else:
                # Otherwise update the list attributes by retaining any
                # elements that have matching 'type' and 'description'
                # values
                new_list = retain_list(
                    slot_info, attr, ['type', 'description']
                )
                setattr(self, attr_name, new_list)

    # -------------------
    #  Protected Methods
    # -------------------

    def __getstate__(self):
        state = pop_dunder_recursive(super().__getstate__())
        state["input_slot_info"] = [
            x.__getstate__() for x in self.input_slot_info
        ]
        state["output_slot_info"] = [
            x.__getstate__() for x in self.output_slot_info
        ]

        return state

    # -------------------
    #   Private Methods
    # -------------------

    def _return_slots(self):
        """Returns slots generated by the DataSource associated with the
        assigned factory attribute"""

        data_source = self.factory.create_data_source()

        try:
            input_slots, output_slots = data_source.slots(self)
        except Exception:
            logger.exception(
                "Unable to retrieve slot information from data source"
                " created by factory {}, plugin {}. This might "
                "indicate a programming error.",
                self.factory.id,
                self.factory.plugin_id
            )
            raise

        return list(input_slots), list(output_slots)

    def _slot_info_generator(self):
        """Generates default lists of InputSlotInfo and
        OutputSlotInfo objects, based on length and attributes of
        Slots tuple returned by _return_slots method"""

        input_slots, output_slots = self._return_slots()

        input_slot_info = [
            InputSlotInfo(type=slot.type,
                          description=slot.description)
            for slot in input_slots
        ]

        output_slot_info = [
            OutputSlotInfo(type=slot.type,
                           description=slot.description)
            for slot in output_slots
        ]

        for element in zip(["input_slot_info", "output_slot_info"],
                           [input_slot_info, output_slot_info]):
            yield element

    def _assign_slot_info(self):
        """Assign input_slot_info or output_slot_info attributes
        with new values, based on the format of return Slot objects
        from _generate_slot methods.

        Raises
        ------
        RuntimeError, if length of slot_info and name attribute are not equal,
        or if the `type` and `description` attributes on each element do not
        pass a `merge_trait_check` call
        """

        # Get default slot info lists and cycle through each slot_info
        # attribute
        for attr_name, slot_info in self._slot_info_generator():

            attr = getattr(self, attr_name)

            if attr:
                # Check that the length of attr is same as its
                # default value
                if len(attr) != len(slot_info):
                    error_msg = (
                        "The number of {} objects ({}) of the"
                        " {} model doesn't match the expected number "
                        "of slots ({}). This is likely due to a "
                        "corrupted file.".format(
                            type(attr[0]).__name__,
                            len(attr),
                            type(self).__name__,
                            len(slot_info))
                    )
                    logger.exception(error_msg)
                    raise RuntimeError(error_msg)

                # Perform a merge of `type` and `description`
                # attributes between the corresponding
                # InputSlotInfo/OutputSlotInfo and Slot elements.
                merge_lists_with_check(
                    attr, slot_info,
                    attributes=['type', 'description']
                )
            else:
                # If attribute list is empty, simply assign default
                # value
                setattr(self, attr_name, slot_info)

    # -------------------
    #   Public Methods
    # -------------------

    def verify(self):
        """ Verify the data source model.

        The data source model must have:
        - input and output slots match between instance and model
        - all output slots named
        - no errors in input or output slots

        Returns
        -------
        errors : list of VerifierErrors
            The list of all detected errors in the data source model.
        """

        input_slots, output_slots = self._return_slots()

        errors = []

        if len(input_slots) != len(self.input_slot_info):
            errors.append(
                VerifierError(
                    subject=self,
                    local_error="The number of input slots is incorrect.",
                    global_error=(
                        "A data source model has incorrect number "
                        "of input slots."
                    ),
                )
            )

        for input_slot in self.input_slot_info:
            errors += input_slot.verify()

        if len(output_slots) != len(self.output_slot_info):
            errors.append(
                VerifierError(
                    subject=self,
                    local_error="The number of output slots is incorrect.",
                    global_error=(
                        "A data source model has incorrect number "
                        "of output slots."
                    ),
                )
            )

        if self.output_slot_info and not any(
                output_slot.name for output_slot in self.output_slot_info):
            errors.append(
                VerifierError(
                    subject=self,
                    severity='warning',
                    local_error="All output variables have undefined names.",
                    global_error=(
                        "A data source model has no defined output names."
                    ),
                )
            )
        for output_slot in self.output_slot_info:
            errors += output_slot.verify()

        return errors
