import abc
from traits.api import ABCHasStrictTraits, provides, String, Instance
from envisage.plugin import Plugin

from .i_data_source_factory import IDataSourceFactory


@provides(IDataSourceFactory)
class BaseDataSourceFactory(ABCHasStrictTraits):
    """Base class for DataSource factories. Reimplement this class to
    create your own DataSource.
    """
    # NOTE: changes to this class must be ported also to the IDataSourceFactory

    #: Unique identifier that identifies the factory uniquely in the
    #: universe of factories. Create one with the function factory_id()
    id = String()

    #: A human readable name of the factory. Spaces allowed
    name = String()

    #: Reference to the plugin that carries this factory
    plugin = Instance(Plugin)

    def __init__(self, plugin, *args, **kwargs):
        self.plugin = plugin
        super(BaseDataSourceFactory, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def create_data_source(self):
        """Factory method.
        Must return the factory-specific BaseDataSource instance.

        Returns
        -------
        BaseDataSource
            The specific instance of the generated DataSource
        """

    @abc.abstractmethod
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