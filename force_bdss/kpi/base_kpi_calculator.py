import abc

from traits.api import ABCHasStrictTraits, Instance

from .i_kpi_calculator_bundle import IKPICalculatorBundle


class BaseKPICalculator(ABCHasStrictTraits):
    """Base class for the KPICalculators.

    Inherit this class for your KPI calculator.
    """
    #: A reference to the bundle
    bundle = Instance(IKPICalculatorBundle)

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseKPICalculator, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def run(self, model, data_source_results):
        """
        Executes the KPI evaluation and returns the results it computes.
        Reimplement this method in your specific KPI calculator.

        Parameters
        ----------
        model: BaseKPICalculatorModel
            The model of the KPI Calculator, instantiated through
            create_model()

        data_source_results:
            a list of DataSourceResult instances containing the results of the
            evaluation. Each DataSourceResult contains the results from one
            specific DataSource.

        Returns
        -------
        KPICalculatorResult
            Instance that holds the results computed by this KPICalculator.
        """
