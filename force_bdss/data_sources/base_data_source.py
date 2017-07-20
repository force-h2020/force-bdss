from traits.api import ABCHasStrictTraits, Instance
import abc

from .base_data_source_model import BaseDataSourceModel
from ..bdss_application import BDSSApplication
from ..data_sources.i_data_source_bundle import IDataSourceBundle


class BaseDataSource(ABCHasStrictTraits):
    """Base class for the DataSource, any computational engine/retriever
    for data.

    Inherit from this class for your specific DataSource.
    """
    #: A reference to the bundle
    bundle = Instance(IDataSourceBundle)
    #: A reference to the application
    application = Instance(BDSSApplication)
    #: A reference to the model class
    model = Instance(BaseDataSourceModel)

    def __init__(self, bundle, application, model, *args, **kwargs):
        self.bundle = bundle
        self.application = application
        self.model = model
        super(BaseDataSource, self).__init__(*args, **kwargs)

    @property
    def name(self):
        """Utility property to retrieve the bundle name from the data source
        object."""
        return self.bundle.name

    @abc.abstractmethod
    def run(self, parameters):
        """Executes the data source evaluation/fetching and returns
        the list of results as a DataSourceResult instance."""
