import logging
from traits.api import provides, Type

from force_bdss.core.base_factory import BaseFactory
from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.data_sources.i_data_source_factory import IDataSourceFactory

log = logging.getLogger(__name__)


@provides(IDataSourceFactory)
class BaseDataSourceFactory(BaseFactory):
    """Base class for DataSource factories. Reimplement this class to
    create your own DataSource.

    You must reimplement the following methods as from example::

        class MyDataSourceFactory(BaseDataSourceFactory)
            def get_data_source_class(self):
                return MyDataSource

            def get_data_source_model(self):
                return MyDataSourceModel

            def get_name(self):
                return "My data source"

            def get_identifier(self):
                return "my_data_source"
    """
    # NOTE: changes to this class must be ported also to the IDataSourceFactory

    #: The data source to be instantiated. Define this to your DataSource
    data_source_class = Type(BaseDataSource, allow_none=False)

    #: The model associated to the data source.
    #: Define this to your DataSourceModel
    model_class = Type(BaseDataSourceModel, allow_none=False)

    def __init__(self, plugin):
        super(BaseDataSourceFactory, self).__init__(plugin=plugin)

        self.data_source_class = self.get_data_source_class()
        self.model_class = self.get_model_class()

    def get_data_source_class(self):
        """Must be reimplemented to return the DataSource class.
        """
        raise NotImplementedError(
            "get_data_source_class was not implemented in factory {}".format(
                self.__class__))

    def get_model_class(self):
        """Must be reimplemented to return the DataSourceModel class.
        """
        raise NotImplementedError(
            "get_model_class was not implemented in factory {}".format(
                self.__class__))

    def create_data_source(self):
        """Factory method.
        Must return the factory-specific BaseDataSource instance.

        Returns
        -------
        BaseDataSource
            The specific instance of the generated DataSource
        """
        return self.data_source_class(self)

    def create_model(self, model_data=None):
        """Factory method.
        Creates the model object (or network of model objects) of the KPI
        calculator. The model can provide a traits UI View according to
        traitsui specifications, so that a UI can be provided automatically.

        Parameters
        ----------
        model_data: dict or None
            A dictionary containing the information to recreate the model.
            If None, an empty (with defaults) model will be returned.

        Returns
        -------
        BaseDataSourceModel
            The model
        """
        if model_data is None:
            model_data = {}

        return self.model_class(self, **model_data)
