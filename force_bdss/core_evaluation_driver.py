import sys
import logging

from traits.api import on_trait_change

from force_bdss.execution import execute_workflow
from force_bdss.ids import InternalPluginID
from .base_core_driver import BaseCoreDriver


log = logging.getLogger(__name__)


class CoreEvaluationDriver(BaseCoreDriver):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """
    id = InternalPluginID.CORE_EVALUATION_DRIVER_ID

    @on_trait_change("application:started")
    def application_started(self):
        try:
            workflow = self.workflow
        except Exception:
            log.exception("Unable to open workflow file.")
            sys.exit(1)

        mco_model = workflow.mco
        if mco_model is None:
            log.info("No MCO defined. Nothing to do. Exiting.")
            sys.exit(0)

        mco_factory = mco_model.factory
        log.info("Creating communicator")
        try:
            mco_communicator = mco_factory.create_communicator()
        except Exception:
            log.exception(
                "Unable to create communicator from MCO factory '{}' "
                "in plugin '{}'. This may indicate a programming "
                "error in the plugin".format(
                    mco_factory.id,
                    mco_factory.plugin.id))
            raise

        mco_data_values = _get_data_values_from_mco(
            mco_model, mco_communicator)

        kpi_results = execute_workflow(workflow, mco_data_values)

        mco_communicator.send_to_mco(mco_model, kpi_results)


def _get_data_values_from_mco(model, communicator):
    """Helper method.
    Receives the data (in order) from the MCO, and bind them to the
    specified names as from the model.

    Parameters
    ----------
    model: BaseMCOModel
        the MCO model (where the user-defined variable names are specified)
    communicator: BaseMCOCommunicator
        The communicator that produces the (temporarily unnamed) datavalues
        from the MCO.
    """
    mco_data_values = communicator.receive_from_mco(model)

    log.info("Received data from MCO: \n{}".format(
             "\n".join([str(x) for x in mco_data_values])))

    if len(mco_data_values) != len(model.parameters):
        error_txt = ("The number of data values returned by"
                     " the MCO ({} values) does not match the"
                     " number of parameters specified ({} values)."
                     " This is either a MCO plugin error or the workflow"
                     " file is corrupted.").format(
            len(mco_data_values), len(model.parameters)
        )
        log.error(error_txt)
        raise RuntimeError(error_txt)

    # The data values obtained by the communicator are unnamed.
    # Assign the name to each datavalue as specified by the user.
    for dv, param in zip(mco_data_values, model.parameters):
        dv.name = param.name

    # Exclude those who have no name set.
    return [dv for dv in mco_data_values if dv.name != ""]
