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
    def run(self, model, slot_values):
        """
        Executes the KPI evaluation and returns the results it computes.
        Reimplement this method in your specific KPI calculator.

        Parameters
        ----------
        model: BaseDataSourceModel
            The model of the DataSource, instantiated through create_model()

        parameters: DataSourceParameters
            a DataResultParameters instance containing the information coming
            from the MCO

        Returns
        -------
        DataSourceResult
            Instance that holds the results computed by this DataSource.
        """

    @abc.abstractmethod
    def slots(self, model):
        """Returns the input (and output) slots of the DataSource.
        Slots are the entities that are needed (and produced) by this
        DataSource.

        The slots may depend on the configuration options, and thus the model.
        This allows, for example, to change the slots depending if an option
        is enabled or not.

        Parameters
        ----------
        model: BaseDataSourceModel
            The model of the DataSource, instantiated through create_model()

        Returns
        -------
        list[tuple, tuple]
            A list containing two tuples, the first element is the input slots,
            the second element is the output slots. Each slot must be an
            instance of the Slot class.
        """
