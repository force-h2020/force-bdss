from traits.api import HasStrictTraits, Instance, List

from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.verifier import VerifierError, multi_error_format
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.notification_listeners.base_notification_listener_model \
    import BaseNotificationListenerModel


class Workflow(HasStrictTraits):
    """Model object that represents the Workflow as a whole"""
    #: Contains the factory-specific MCO Model object.
    #: Can be None if no MCO has been specified yet.
    mco = Instance(BaseMCOModel, allow_none=True)

    #: The execution layers. Execution starts from the first layer,
    #: where all data sources are executed in sequence. It then passes all
    #: the computed data to the second layer, then the third etc.
    execution_layers = List(ExecutionLayer)

    #: Contains information about the listeners to be setup
    notification_listeners = List(BaseNotificationListenerModel)

    def verify(self):
        """ Verify the workflow.

        The workflow must have:
        - an MCO
        - at least one execution layer
        - no errors in the MCO or any execution layer

        Returns
        -------
        errors : list of VerifierErrors
            The list of all detected errors in the workflow.
        """
        errors = []

        if not self.mco:
            errors.append(
                VerifierError(
                    subject=self,
                    global_error="Workflow has no MCO",
                )
            )
        else:
            errors += self.mco.verify()

        if not self.execution_layers:
            errors.append(
                VerifierError(
                    subject=self,
                    global_error="Workflow has no execution layers",
                )
            )
        else:
            for layer in self.execution_layers:
                errors += layer.verify()
            missing_layers = [
                i for i, layer in enumerate(self.execution_layers)
                if not layer.data_sources
            ]
            if len(missing_layers) == 1:
                errors.append(
                    VerifierError(
                        subject=self,
                        global_error="Layer {} has no data sources".format(
                            missing_layers[0]
                        ),
                    )
                )
            elif len(missing_layers) > 1:
                errors.append(
                    VerifierError(
                        subject=self,
                        global_error="Layers {} have no data sources".format(
                            multi_error_format(missing_layers)
                        ),
                    )
                )

        return errors