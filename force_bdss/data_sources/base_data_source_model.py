from copy import deepcopy
from logging import getLogger

from traits.api import (
    Instance, List, Event, on_trait_change
)

from force_bdss.core.base_model import BaseModel
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.core.verifier import VerifierError
from force_bdss.data_sources.i_data_source_factory import IDataSourceFactory


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
        try:
            data_source = self.factory.create_data_source()
        except Exception:
            logger.exception(
                "Unable to create data source from factory '%s', plugin "
                "'%s'. This might indicate a  programming error",
                self.factory.id,
                self.factory.plugin_id,
            )
            raise

        try:
            input_slots, output_slots = data_source.slots(self)
        except Exception:
            logger.exception(
                "Unable to retrieve slot information from data source"
                " created by factory '%s', plugin '%s'. This might "
                "indicate a programming error.",
                self.factory.id,
                self.factory.plugin_id
            )
            raise

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
                    local_error="All output variables have undefined names",
                    global_error=(
                        "A data source model has no defined output names"
                    ),
                )
            )
        for output_slot in self.output_slot_info:
            errors += output_slot.verify()

        return errors

    @on_trait_change("+changes_slots")
    def _trigger_changes_slots(self, obj, name, new):
        changes_slots = self.traits()[name].changes_slots

        if changes_slots:
            self.changes_slots = True

    @classmethod
    def from_json(cls, factory, json_data):
        """ Instantiate an BaseMCOModel object from a `json_data`
        dictionary and the generating `factory` object.

        Parameters
        ----------
        factory: IDataSourceFactory
            Generating factory object
        json_data: dict
            Dictionary with a DataSourceModel serialized data

        Returns
        ----------
        layer: BaseDataSourceModel
            BaseDataSourceModel instance with attributes values from
            the `json_data` dict
        """
        data = deepcopy(json_data)

        input_slots = [InputSlotInfo(**d) for d in data["input_slot_info"]]
        data["input_slot_info"] = input_slots

        output_slots = [OutputSlotInfo(**d) for d in data["output_slot_info"]]
        data["output_slot_info"] = output_slots

        data_source = cls(factory=factory, **data)
        return data_source
