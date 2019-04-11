from traits.api import HasStrictTraits, provides

from i_operation import IOperation


@provides(IOperation)
class EvaluateOperation(HasStrictTraits):

    #: The workflow file being operated on.
    workflow_file = Instance(WorkflowFile)

    #: The workflow instance.
    workflow = DelegegatesTo('workflow_file')

    def run(self):
        """ Evaluate the workflow. """
        mco_model = self.workflow.mco
        if mco_model is None:
            log.info("No MCO defined. Nothing to do. Exiting.")
            return

        mco_factory = mco_model.factory

        log.info("Creating communicator")
        try:
            mco_communicator = mco_factory.create_communicator()
        except Exception:
            log.exception((
                "Unable to create communicator from MCO factory '' "
                "in plugin '{}'. This may indicate a programming "
                "error in the plugin").format(
                    mco_factory.id,
                    mco_factory.plugin.id))
            return False

        mco_data_values = mco_communicator.receive_from_mco(mco_model)

        kpi_results = workflow.execute(mco_data_values)

        mco_communicator.send_to_mco(mco_model, kpi_results)
