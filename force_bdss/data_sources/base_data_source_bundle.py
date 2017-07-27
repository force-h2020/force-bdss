import abc
from traits.api import ABCHasStrictTraits, provides, String, Instance
from envisage.plugin import Plugin

from .i_data_source_bundle import IDataSourceBundle


@provides(IDataSourceBundle)
class BaseDataSourceBundle(ABCHasStrictTraits):
    """Base class for DataSource bundles. Reimplement this class to
    create your own DataSource.
    """
    # NOTE: changes to this class must be ported also to the IDataSourceBundle

    #: Unique identifier that identifies the bundle uniquely in the
    #: universe of bundles. Create one with the function bundle_id()
    id = String()

    #: A human readable name of the bundle. Spaces allowed
    name = String()

    plugin = Instance(Plugin)

    def __init__(self, plugin, *args, **kwargs):
        self.plugin = plugin
        super(BaseDataSourceBundle, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def create_data_source(self):
        """Factory method.
        Must return the bundle-specific BaseDataSource instance.

        Parameters
        ----------
        application: Application
            The envisage application.
        model: BaseDataSourceModel
            The model of the data source, instantiated with create_model()

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
