from traits.has_traits import on_trait_change

from force_bdss.base_core_driver import BaseCoreDriver


class CoreEvaluationDriver(BaseCoreDriver):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    @on_trait_change("application:started")
    def application_started(self):
        workflow = self.application.workflow

        mco_data = workflow.multi_criteria_optimizer
        mco_bundle = self._mco_bundle_by_id(mco_data.id)
        mco_model = mco_bundle.create_model(mco_data.model_data)
        mco_communicator = mco_bundle.create_communicator(
            self.application,
            mco_model)

        parameters = mco_communicator.receive_from_mco()

        ds_results = []
        for requested_ds in workflow.data_sources:
            ds_bundle = self._data_source_bundle_by_id(
                requested_ds.id)
            ds_model = ds_bundle.create_model(requested_ds.model_data)
            data_source = ds_bundle.create_data_source(
                self.application, ds_model)
            ds_results.append(data_source.run(parameters))

        kpi_results = []
        for requested_kpic in workflow.kpi_calculators:
            kpic_bundle = self._kpi_calculator_bundle_by_id(
                requested_kpic.id)
            ds_model = kpic_bundle.create_model(
                requested_kpic.model_data)
            kpi_calculator = kpic_bundle.create_data_source(
                self.application, ds_model)
            kpi_results.append(kpi_calculator.run(ds_results))

        mco_communicator.send_to_mco(kpi_results)
