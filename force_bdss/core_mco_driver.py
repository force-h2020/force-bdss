from __future__ import print_function

import sys

from traits.api import on_trait_change

from force_bdss.base_core_driver import BaseCoreDriver
from force_bdss.io.workflow_reader import (InvalidVersionException,
                                           InvalidFileException)


class CoreMCODriver(BaseCoreDriver):
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
        mco = mco_bundle.create_optimizer(self.application, mco_model)
        mco.run()
