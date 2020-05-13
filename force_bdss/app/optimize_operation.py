#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import logging

from traits.api import provides
from .i_operation import IOperation
from .base_operation import BaseOperation

log = logging.getLogger(__name__)


@provides(IOperation)
class OptimizeOperation(BaseOperation):
    """Performs a full MCO run on a system described by a `Workflow`
    object, based on the format given by a `BaseMCO` class. Contains
    optional `NotificationListener` classes in order to broadcast
    information during the MCO run."""

    def run(self):
        """ Create and run the optimizer.
        """

        # Verify the workflow
        self.verify_workflow()

        # Create the optimizer
        mco = self.create_mco()

        # Set up listeners
        self._initialize_listeners()
        self._deliver_start_event()

        try:
            mco.run(self.workflow)
        except Exception:
            log.exception(
                (
                    "Method run() of MCO with id '{}' from plugin '{}' "
                    "raised exception. This might indicate a "
                    "programming error in the plugin."
                ).format(mco.factory.id, mco.factory.plugin_id)
            )
            raise
        finally:
            # Tear down listeners
            self._deliver_finish_event()
            self._finalize_listeners()

    def create_mco(self):
        """ Create the MCO from the model's factory. """
        mco_factory = self.workflow.mco_model.factory
        try:
            mco = mco_factory.create_optimizer()
        except Exception:
            log.exception(
                (
                    "Unable to instantiate optimizer for mco '{}' in "
                    "plugin '{}'. An exception was raised. "
                    "This might indicate a programming error in the "
                    "plugin."
                ).format(mco_factory.id, mco_factory.plugin_id)
            )
            raise

        return mco
