from copy import deepcopy
import logging

from traits.api import HasStrictTraits, List, on_trait_change

from force_bdss.core.data_value import DataValue
from force_bdss.core.verifier import VerifierError
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.events.event_notifier_mixin import EventNotifierMixin
from force_bdss.utilities import pop_dunder_recursive, nested_getstate

log = logging.getLogger(__name__)


class ExecutionLayer(EventNotifierMixin, HasStrictTraits):
    """Represents a single layer in the execution stack.
    It contains a list of the data source models that must be executed.
    """

    #: The data sources in the execution layer.
    data_sources = List(BaseDataSourceModel)

    def execute_layer(self, environment_data_values):
        """ Performs the evaluation of a single layer.

        Parameters
        ----------
        environment_data_values: list
            A list of data values to submit to the evaluators.

        NOTE: The above parameter is going to go away as soon as we move
        to unlimited layers and remove the distinction between data sources
        and KPI calculators.
        """
        results = []

        for model in self.data_sources:
            factory = model.factory
            try:
                data_source = factory.create_data_source()
            except Exception:
                log.exception(
                    "Unable to create data source from factory '{}' "
                    "in plugin '{}'. This may indicate a programming "
                    "error in the plugin".format(factory.id, factory.plugin_id)
                )
                raise

            # Get the slots for this data source. These must be matched to
            # the appropriate values in the environment data values.
            # Matching is by position.
            in_slots, out_slots = data_source.slots(model)

            # Binding performs the extraction of the specified data values
            # satisfying the above input slots from the environment data values
            # considering what the user specified in terms of names (which is
            # in the model input slot info
            # The resulting data are the ones picked by name from the
            # environment data values, and in the appropriate ordering as
            # needed by the input slots.
            passed_data_values = _bind_data_values(
                environment_data_values, model.input_slot_info, in_slots
            )

            # execute data source, passing only relevant data values.
            log.info("Evaluating for Data Source {}".format(factory.name))
            log.info("Passed values:")
            for idx, dv in enumerate(passed_data_values):
                log.info("{}: {}".format(idx, dv))

            try:
                res = data_source._run(model, passed_data_values)
            except Exception:
                log.exception(
                    "Evaluation could not be performed. "
                    "Run method raised exception."
                )
                raise

            if not isinstance(res, list):
                error_txt = (
                    "The run method of data source {} must return a list."
                    " It returned instead {}. Fix the run() method to return"
                    " the appropriate entity.".format(factory.name, type(res))
                )
                log.error(error_txt)
                raise RuntimeError(error_txt)

            if len(res) != len(out_slots):
                error_txt = (
                    "The number of data values ({} values) returned"
                    " by '{}' does not match the number"
                    " of output slots it specifies ({} values)."
                    " This is likely a plugin error."
                ).format(len(res), factory.name, len(out_slots))
                log.error(error_txt)
                raise RuntimeError(error_txt)

            for idx, dv in enumerate(res):
                if not isinstance(dv, DataValue):
                    error_txt = (
                        "The result list returned by DataSource {} contains"
                        " an entry that is not a DataValue. An entry of type"
                        " {} was instead found in position {}."
                        " Fix the DataSource.run() method"
                        " to return the appropriate entity.".format(
                            factory.name, type(dv), idx
                        )
                    )
                    log.error(error_txt)
                    raise RuntimeError(error_txt)

            # At this point, the returned data values are unnamed.
            # Add the names as specified by the user.
            for dv, output_slot_info in zip(res, model.output_slot_info):
                dv.name = output_slot_info.name

            # If the name was not specified, simply discard the value,
            # because apparently the user is not interested in it.
            res = [r for r in res if r.name != ""]
            results.extend(res)

            log.info("Returned values:")
            for idx, dv in enumerate(res):
                log.info("{}: {}".format(idx, dv))

        # Finally, return all the computed data values from all evaluators,
        # properly named.
        return results

    def verify(self):
        """ Verify an ExecutionLayer.

        The execution layer must have:
        - at least one data source
        - no errors in any data source

        Returns
        -------
        errors : list of VerifierErrors
            The list of all detected errors in the execution layer.
        """
        errors = []

        if not self.data_sources:
            errors.append(
                VerifierError(
                    subject=self,
                    severity="warning",
                    trait_name="data_sources",
                    local_error="Layer has no data sources",
                    global_error="An execution layer has no data sources",
                )
            )
        for data_source in self.data_sources:
            errors += data_source.verify()

        return errors

    def __getstate__(self):
        state = pop_dunder_recursive(super().__getstate__())
        state = nested_getstate(state)
        return state

    @classmethod
    def from_json(cls, factory_registry, json_data):
        """ Instantiate an ExecutionLayer object from a `json_data`
        dictionary and the generating `factory_registry`.
        If the `json_data` is an empty dict, the `data_sources`
        attribute will be an empty list.

        Parameters
        ----------
        factory_registry: Instance(IFactoryRegistry)
            Generating factory registry
        json_data: dict
            Dictionary with an execution layer serialized data

        Returns
        ----------
        layer: ExecutionLayer
            ExecutionLayer instance with attributes values from
            the `json_data` dict
        """
        data = deepcopy(json_data)

        models = []
        for data_source in data.get("data_sources", []):
            id = data_source["id"]
            data_source_factory = factory_registry.data_source_factory_by_id(
                id
            )
            model = data_source_factory.model_class.from_json(
                data_source_factory, data_source["model_data"]
            )
            models.append(model)
        data["data_sources"] = models

        layer = cls(**data)
        return layer

    @on_trait_change("data_sources:event")
    def notify_driver_event(self, event):
        """ Captures a BaseDriverEvent and passes it on to a Workflow

        Parameters
        ----------
        event: BaseDriverEvent
            The BaseDriverEvent that has been changed
        """
        self.notify(event)


def _bind_data_values(available_data_values, model_slot_map, slots):
    """
    Given the named data values in the environment, the slots a given
    data source expects, and the user-specified names for each of these
    slots, returns those data values with the requested names, ordered
    in the correct order as specified by the slot map.
    """
    passed_data_values = []
    lookup_map = {dv.name: dv for dv in available_data_values}

    if len(slots) != len(model_slot_map):
        raise RuntimeError(
            "The length of the slots is not equal to"
            " the length of the slot map. This may"
            " indicate a file error."
        )

    try:
        for slot, slot_map in zip(slots, model_slot_map):
            passed_data_values.append(lookup_map[slot_map.name])
    except KeyError:
        raise RuntimeError(
            "Unable to find requested name '{}' in available "
            "data values. Current data value names: {}".format(
                slot_map.name, list(lookup_map.keys())
            )
        )

    return passed_data_values
