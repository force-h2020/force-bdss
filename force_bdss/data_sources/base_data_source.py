import abc
import six


class BaseDataSource(six.with_metaclass(abc.ABCMeta)):
    """Base class for the DataSource, any computational engine/retriever
    for data.

    Inherit from this class for your specific DataSource.
    """
    def __init__(self, bundle, application, model):
        self.bundle = bundle
        self.application = application
        self.model = model

    @property
    def name(self):
        return self.bundle.name

    @abc.abstractmethod
    def run(self, parameters):
        """Executes the data source evaluation/fetching and returns
        the list of results as a DataSourceResult instance."""
        pass
