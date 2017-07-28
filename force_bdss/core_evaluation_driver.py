from __future__ import print_function

import sys
from traits.api import on_trait_change

from .ids import plugin_id
from .base_core_driver import BaseCoreDriver
from .io.workflow_reader import (
    InvalidVersionException,
    InvalidFileException
)

CORE_EVALUATION_DRIVER_ID = plugin_id("core", "CoreEvaluationDriver")


class CoreEvaluationDriver(BaseCoreDriver):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """
    id = CORE_EVALUATION_DRIVER_ID

    @on_trait_change("application:started")
    def application_started(self):
        try:
            workflow = self.workflow
        except (InvalidVersionException, InvalidFileException) as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        mco_model = workflow.mco
        mco_bundle = mco_model.bundle
        mco_communicator = mco_bundle.create_communicator()

        parameters = mco_communicator.receive_from_mco(mco_model)

        ds_results = []
        for ds_model in workflow.data_sources:
            ds_bundle = ds_model.bundle
            data_source = ds_bundle.create_data_source()
            ds_results.append(data_source.run(ds_model, parameters))

        kpi_results = []
        for kpic_model in workflow.kpi_calculators:
            kpic_bundle = kpic_model.bundle
            kpi_calculator = kpic_bundle.create_kpi_calculator()
            kpi_results.append(kpi_calculator.run(kpic_model, ds_results))

        mco_communicator.send_to_mco(mco_model, kpi_results)
