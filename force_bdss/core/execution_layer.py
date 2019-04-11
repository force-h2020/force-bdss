from traits.api import HasStrictTraits, List

from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel


class ExecutionLayer(HasStrictTraits):
    """Represents a single layer in the execution stack.
    It contains a list of the data source models that must be executed.
    """
    data_sources = List(BaseDataSourceModel)

    def execute_layer(self, environment_data_values):
        """Helper routine.
        Performs the evaluation of a single layer.
        At the moment we have a single layer of DataSources followed
        by a single layer of KPI calculators.

        Parameters
        ----------
        layer: ExecutionLayer
            A list of the models for all the data sources

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
                    "error in the plugin".format(
                        factory.id,
                        factory.plugin.id))
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
                environment_data_values,
                model.input_slot_info,
                in_slots)

            # execute data source, passing only relevant data values.
            log.info("Evaluating for Data Source {}".format(
                factory.name))
            log.info("Passed values:")
            for idx, dv in enumerate(passed_data_values):
                log.info("{}: {}".format(idx, dv))

            try:
                res = data_source.run(model, passed_data_values)
            except Exception:
                log.exception(
                    "Evaluation could not be performed. "
                    "Run method raised exception.")
                raise

            if not isinstance(res, list):
                error_txt = (
                    "The run method of data source {} must return a list."
                    " It returned instead {}. Fix the run() method to return"
                    " the appropriate entity.".format(
                        factory.name,
                        type(res)
                    ))
                log.error(error_txt)
                raise RuntimeError(error_txt)

            if len(res) != len(out_slots):
                error_txt = (
                    "The number of data values ({} values) returned"
                    " by '{}' does not match the number"
                    " of output slots it specifies ({} values)."
                    " This is likely a plugin error.").format(
                    len(res), factory.name, len(out_slots)
                )

                log.error(error_txt)
                raise RuntimeError(error_txt)

            if len(res) != len(model.output_slot_info):
                error_txt = (
                    "The number of data values ({} values) returned"
                    " by '{}' does not match the number"
                    " of user-defined names specified ({} values)."
                    " This is either a plugin error or a file"
                    " error.").format(
                    len(res),
                    factory.name,
                    len(model.output_slot_info)
                )

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
                            factory.name,
                            type(dv),
                            idx
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
