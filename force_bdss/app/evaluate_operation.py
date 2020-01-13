import logging

from traits.api import DelegatesTo, HasStrictTraits, Instance, provides

from .i_operation import IOperation
from .workflow_file import WorkflowFile


log = logging.getLogger(__name__)


@provides(IOperation)
class EvaluateOperation(HasStrictTraits):
    """Performs the evaluation of a single point in an MCO,
    based on the system described by a `Workflow` object.
    """

    #: The workflow file being operated on.
    workflow_file = Instance(WorkflowFile)

    #: The workflow instance.
    workflow = DelegatesTo('workflow_file')

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
