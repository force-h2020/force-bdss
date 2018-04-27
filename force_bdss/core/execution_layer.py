from traits.api import HasStrictTraits, List

from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel


class ExecutionLayer(HasStrictTraits):
    """Represents a single layer in the execution stack.
    It contains a list of the data source models that must be executed.
    """
    data_sources = List(BaseDataSourceModel)
