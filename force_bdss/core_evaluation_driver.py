import sys
from traits.api import on_trait_change

from force_bdss.base_core_driver import BaseCoreDriver
from force_bdss.io.workflow_reader import InvalidVersionException, \
    InvalidFileException


class CoreEvaluationDriver(BaseCoreDriver):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    @on_trait_change("application:started")
    def application_started(self):
        try:
            workflow = self.workflow
        except (InvalidVersionException, InvalidFileException) as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        mco_model = workflow.multi_criteria_optimizer
        mco_bundle = mco_model.bundle
        mco_communicator = mco_bundle.create_communicator(
            self.application,
            mco_model)

        parameters = mco_communicator.receive_from_mco()

        ds_results = []
        for ds_model in workflow.data_sources:
            ds_bundle = ds_model.bundle
            data_source = ds_bundle.create_data_source(self.application,
                                                       ds_model)
            ds_results.append(data_source.run(parameters))

        kpi_results = []
        for kpic_model in workflow.kpi_calculators:
            kpic_bundle = kpic_model.bundle
            kpi_calculator = kpic_bundle.create_kpi_calculator(
                self.application, kpic_model)
            kpi_results.append(kpi_calculator.run(ds_results))

        mco_communicator.send_to_mco(kpi_results)
