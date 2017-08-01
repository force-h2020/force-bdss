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
        """
        Executes the Data Source evaluation and returns the results it
        computes. Reimplement this method in your specific DataSource.

        Parameters
        ----------
        model: BaseDataSourceModel
            The model of the DataSource, instantiated through create_model()

        parameters: List(DataValue)
            a list of DataValue objects containing the information needed
            for the execution of the DataSource.

        Returns
        -------
        List(DataValue)
            A list containing the computed Data Values.
        """
