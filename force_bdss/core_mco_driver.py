import sys

from traits.api import on_trait_change

from force_bdss.base_core_driver import BaseCoreDriver
from force_bdss.workspecs.workflow import InvalidVersionException


class CoreMCODriver(BaseCoreDriver):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    @on_trait_change("application:started")
    def application_started(self):
        try:
            workflow = self.application.workflow
        except InvalidVersionException as e:
            print e.message
            sys.exit(1)

        mco_data = workflow.multi_criteria_optimizer
        mco_bundle = self.bundle_registry.mco_bundle_by_id(mco_data.id)
        mco_model = mco_bundle.create_model(mco_data.model_data)
        mco = mco_bundle.create_optimizer(self.application, mco_model)

        mco.run()
