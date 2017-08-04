import abc

from traits.api import ABCHasStrictTraits, Instance

from .i_kpi_calculator_factory import IKPICalculatorFactory


class BaseKPICalculator(ABCHasStrictTraits):
    """Base class for the KPICalculators.

    Inherit this class for your KPI calculator.
    """
    #: A reference to the factory
    factory = Instance(IKPICalculatorFactory)

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        super(BaseKPICalculator, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def run(self, model, data_values):
        """
        Executes the KPI evaluation and returns the results it computes.
        Reimplement this method in your specific KPI calculator.

        Parameters
        ----------
        model: BaseKPICalculatorModel
            The model of the KPI Calculator, instantiated through
            create_model()

        data_values:
            a list of DataValue instances containing data from the
            MCO and DataSources.

        Returns
        -------
        List[DataValue]:
            The result of this KPI evaluation, as a list of DataValues.
        """

    @abc.abstractmethod
    def slots(self, model):
        """Returns the input (and output) slots of the KPI Calculator.
        Slots are the entities that are needed (and produced) by this
        KPI Calculator.

        The slots may depend on the configuration options, and thus the model.
        This allows, for example, to change the slots depending if an option
        is enabled or not.

        Parameters
        ----------
        model: BaseKPICalculatorModel
            The model of the KPICalculator, instantiated through create_model()

        Returns
        -------
        (input_slots, output_slots): tuple[tuple, tuple]
            A tuple containing two tuples.
            The first element is the input slots, the second element is
            the output slots. Each slot must be an instance of the Slot class.
            It is possible for each of the two inside tuples to be empty.
            The case of an empty input slot is common: the KPICalculator does
            not need any information from the MCO to operate.
            The case of an empty output slot is uncommon, but supported:
            the KPICalculator does not produce any output and is therefore
            useless.
        """
