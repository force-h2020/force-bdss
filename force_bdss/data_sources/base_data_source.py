from traits.api import ABCHasStrictTraits, Instance
import abc

from ..data_sources.i_data_source_bundle import IDataSourceBundle


class BaseDataSource(ABCHasStrictTraits):
    """Base class for the DataSource, any computational engine/retriever
    for data.

    Inherit from this class for your specific DataSource.
    """
    #: A reference to the bundle
    bundle = Instance(IDataSourceBundle)

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseDataSource, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def run(self, model, parameters):
        """Executes the data source evaluation/fetching and returns
        the list of results as a DataSourceResult instance."""
