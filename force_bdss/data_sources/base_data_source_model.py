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

from .data_source_utilities import sync_trait_with_check, retain_list

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

    def __init__(self, factory=None, input_slot_info=None,
                 output_slot_info=None, *args, **kwargs):
        super(BaseDataSourceModel, self).__init__(factory, *args, **kwargs)

        # If either input_slot_info or output_slot_info have been passed in
        # as arguments, perform extra checks before assigning to make sure
        # they will be accepted by the BaseDataSource associated with factory
        if input_slot_info is not None:
            self._assign_slot_info("input_slot_info", input_slot_info)
        if output_slot_info is not None:
            self._assign_slot_info("output_slot_info", output_slot_info)

    # -------------------
    #      Defaults
    # -------------------

    def _input_slot_info_default(self):
        """Default list of InputSlotInfo object, based on length and
        attributes of Slots tuple returned by slots method on associated
        BaseDataSource"""

        input_slots, _ = self._generate_slots()

        return [
            InputSlotInfo(name='',
                          type=slot.type,
                          description=slot.description)
            for slot in input_slots
        ]

    def _output_slot_info_default(self):
        """Default list of OutputSlotInfo object, based on length and
        attributes of Slots tuple returned by slots method on associated
        BaseDataSource"""
        _, output_slots = self._generate_slots()

        return [
            OutputSlotInfo(name='',
                           type=slot.type,
                           description=slot.description)
            for slot in output_slots
        ]

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

        Retains any InputSlotInfo or OutputSlotInfo elements
        referring to variables that have been defined before.
        These are identified as having matching `type` and
        `description` attributes.
        """

        # Get new slots, caused by change_slots event
        new_input_slot_info = self._input_slot_info_default()
        new_output_slot_info = self._output_slot_info_default()

        # Update the input_slot_info and output_slot_info attributes
        # by retaining any slots that already exist and are named in the
        # UI
        self.input_slot_info = retain_list(
            new_input_slot_info, self.input_slot_info,
            ['type', 'description']
        )

        self.output_slot_info = retain_list(
            new_output_slot_info, self.output_slot_info,
            ['type', 'description']
        )

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

    def _generate_slots(self):
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

        return input_slots, output_slots

    def _assign_slot_info(self, name, new_slot_info):
        """Assign either input_slot_info or output_slot_info attributes
        with new values. The argument `new_slot_info` must have the same length
        as the existing `name` attribute. Each element in new_slot_info must also
        contain matching `type`, `description` attributes as the corresponding
        element in the existing `name` attribute.

        Parameters
        ----------
        name: str
            Name of attribute to update, must be either "input_slot_info"
            or "output_slot_info"
        new_slot_info: list of type InputSlotInfo of OutputSlotInfo
            List containing objects to update each element of
            name attribute with

        Raises
        ------
        ValueError, if `name` argument is not either "input_slot_info",
        or "output_slot_info"
        RuntimeError, if length of slot_info and name attribute are not equal,
        or if the `type` and `description` attributes on each element do not
        match
        """

        # Ignore any changes if new_slot_info list is empty
        if len(new_slot_info) == 0:
            return

        # Perform a value check on `name` argument
        if name not in ["input_slot_info", "output_slot_info"]:
            error_msg = (
                "Attribute 'name' must be either 'input_slot_info' "
                "or 'output_slot_info'."
            )
            logger.exception(error_msg)
            raise ValueError(error_msg)

        # Obtain a reference to the old attribute that will be reassigned
        old_slot_info = getattr(self, name)

        # Check that the length of the new attribute is the same
        # as the old
        if len(new_slot_info) != len(old_slot_info):
            error_msg = (
                "The number of slots in {} ({}) of the {} model doesn't"
                " match the expected number of slots ({}). This is"
                " likely due to a corrupted file.".format(
                    name, len(old_slot_info),
                    type(self).__name__,
                    len(new_slot_info))
            )
            logger.exception(error_msg)
            raise RuntimeError(error_msg)

        # Check whether each element in new_slot_info has the same class,
        # `type` and `description` attributes as the corresponding element
        # in old_slot_info, and if so, synchronize their `name` attributes
        for new_info, old_info in zip(new_slot_info, old_slot_info):
            sync_trait_with_check(
                new_info, old_info, 'name',
                attributes=['__class__', 'type', 'description'],
                ignore_default=True
            )

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

        input_slots, output_slots = self._generate_slots()

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
