import logging

from traits.api import provides
from .i_operation import IOperation
from .base_operation import BaseOperation

log = logging.getLogger(__name__)


@provides(IOperation)
class EvaluateOperation(BaseOperation):
    """Performs the evaluation of a single point in an MCO,
    based on the system described by a `Workflow` object.
    """

    def run(self):
        """ Evaluate the workflow.
        """

        # Verify the workflow
        self.verify_workflow()

        # Obtain MCO model and communicator
        mco_model = self.workflow.mco_model
        mco_communicator = self.create_mco_communicator()

        # Set up listeners
        self._initialize_listeners()
        self._deliver_start_event()

        try:
            mco_data_values = mco_communicator.receive_from_mco(mco_model)
            kpi_results = self.workflow.execute(mco_data_values)
            mco_communicator.send_to_mco(mco_model, kpi_results)
        except Exception:
            # Simply propagate any error message that is raised, and
            # ensure that listener and event objects are correctly
            # teared down afterwards.
            raise
        finally:
            # Tear down listeners
            self._deliver_finish_event()
            self._finalize_listeners()

    def create_mco_communicator(self):
        """Create BaseMCOCommunicator instance associated with
        the BaseMCOModel subclass in the Workflow"""
        mco_factory = self.workflow.mco_model.factory

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
            raise

        return mco_communicator
