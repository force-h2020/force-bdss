from traits.api import HasStrictTraits, List

from force_bdss.core.verifier import VerifierError
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel


class ExecutionLayer(HasStrictTraits):
    """Represents a single layer in the execution stack.
    It contains a list of the data source models that must be executed.
    """
    data_sources = List(BaseDataSourceModel)

    def verify(self):
        """ Verify an ExecutionLayer.

        The execution layer must have:
        - at least one data source
        - no errors in any data source

        Returns
        -------
        errors : list of VerifierErrors
            The list of all detected errors in the execution layer.
        """
        errors = []

        if not self.data_sources:
            errors.append(
                VerifierError(
                    subject=self,
                    severity='warning',
                    trait_name='data_sources',
                    local_error="Layer has no data sources",
                    global_error="An execution layer has no data sources",
                )
            )
        for data_source in self.data_sources:
            errors += data_source.verify()

        return errors