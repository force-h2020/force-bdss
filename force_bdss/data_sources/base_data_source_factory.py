import logging
from traits.api import ABCHasStrictTraits, provides, Str, Instance, Type
from envisage.plugin import Plugin

from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.data_sources.i_data_source_factory import IDataSourceFactory
from force_bdss.ids import factory_id

log = logging.getLogger(__name__)


@provides(IDataSourceFactory)
class BaseDataSourceFactory(ABCHasStrictTraits):
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

    #: Unique identifier that identifies the factory uniquely in the
    #: universe of factories. Create one with the function factory_id()
    id = Str()

    #: A human readable name of the factory. Spaces allowed
    name = Str()

    #: The data source to be instantiated. Define this to your DataSource
    data_source_class = Type(BaseDataSource)

    #: The model associated to the data source.
    #: Define this to your DataSourceModel
    model_class = Type(BaseDataSourceModel)

    #: Reference to the plugin that carries this factory
    #: This is automatically set by the system. you should not define it
    #: in your subclass.
    plugin = Instance(Plugin)

    def __init__(self, plugin, *args, **kwargs):
        self.plugin = plugin
        super(BaseDataSourceFactory, self).__init__(*args, **kwargs)

        self.data_source_class = self.get_data_source_class()
        self.model_class = self.get_model_class()
        self.name = self.get_name()
        identifier = self.get_identifier()
        self.id = factory_id(self.plugin.id, identifier)

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

    def get_name(self):
        """Must be reimplemented to return a user-visible name of the
        data source.
        """
        raise NotImplementedError(
            "get_name was not implemented in factory {}".format(
                self.__class__))

    def get_identifier(self):
        """Must be reimplemented to return a unique string identifying
        the factory. The provider is responsible to guarantee this identifier
        to be unique across the plugin data sources.
        """
        raise NotImplementedError(
            "get_name was not implemented in factory {}".format(
                self.__class__))

    def create_data_source(self):
        """Factory method.
        Must return the factory-specific BaseDataSource instance.

        Returns
        -------
        BaseDataSource
            The specific instance of the generated DataSource
        """
        if self.data_source_class is None:
            msg = ("data_source_class cannot be None in {}. Either define "
                   "data_source_class or reimplement create_data_source on "
                   "your factory class.".format(self.__class__.__name__))
            log.error(msg)
            raise RuntimeError(msg)

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

        if self.model_class is None:
            msg = ("model_class cannot be None in {}. Either define "
                   "model_class or reimplement create_model on your "
                   "factory class.".format(self.__class__.__name__))
            log.error(msg)
            raise RuntimeError(msg)

        return self.model_class(self, **model_data)
