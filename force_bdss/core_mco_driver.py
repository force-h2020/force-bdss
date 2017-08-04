from __future__ import print_function

import sys

from traits.api import on_trait_change, Instance

from force_bdss.mco.base_mco import BaseMCO
from .ids import plugin_id
from .base_core_driver import BaseCoreDriver
from .io.workflow_reader import (
    InvalidVersionException,
    InvalidFileException
)

CORE_MCO_DRIVER_ID = plugin_id("core", "CoreMCODriver")


class CoreMCODriver(BaseCoreDriver):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """
    id = CORE_MCO_DRIVER_ID

    mco = Instance(BaseMCO, allow_none=True)

    listeners = Instance(BaseNotificationListener)

    @on_trait_change("application:started")
    def application_started(self):
        try:
            workflow = self.workflow
        except (InvalidVersionException, InvalidFileException) as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        mco_model = workflow.mco
        mco_bundle = mco_model.bundle
        self.mco = mco_bundle.create_optimizer()
        self.mco.run(mco_model)

