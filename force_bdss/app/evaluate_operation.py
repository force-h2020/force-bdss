import logging
import sys

from traits.api import provides, on_trait_change
from .i_operation import IOperation
from .base_operation import BaseOperation

log = logging.getLogger(__name__)


@provides(IOperation)
class EvaluateOperation(BaseOperation):
    """Performs the evaluation of a single point in an MCO,
    based on the system described by a `Workflow` object.
    """

    def run(self):
        """ Evaluate the workflow. """
        mco_model = self.workflow.mco_model
        if mco_model is None:
            log.info("No MCO defined. Nothing to do. Exiting.")
            return

        mco_factory = mco_model.factory

        log.info("Creating communicator")
        try:
            mco_communicator = mco_factory.create_communicator()
        except Exception:
            log.exception((
                "Unable to create communicator from MCO factory '{}'"
                " in plugin '{}'. This may indicate a programming "
                "error in the plugin").format(
                    mco_factory.id,
                    mco_factory.plugin_id))
            return False

        mco_data_values = mco_communicator.receive_from_mco(mco_model)

        kpi_results = self.workflow.execute(mco_data_values)

        mco_communicator.send_to_mco(mco_model, kpi_results)
