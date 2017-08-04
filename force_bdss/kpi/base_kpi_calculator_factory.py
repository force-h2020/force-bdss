import abc
from envisage.plugin import Plugin
from traits.api import ABCHasStrictTraits, provides, String, Instance

from .i_kpi_calculator_factory import IKPICalculatorFactory


@provides(IKPICalculatorFactory)
class BaseKPICalculatorFactory(ABCHasStrictTraits):
    """Base class for the Key Performance Indicator calculator factories.
    Inherit from this class to create a factory, and reimplement the abstract
    methods.
    """
    # NOTE: any changes in this interface must be ported to
    # IKPICalculatorFactory

    #: A unique ID generated with factory_id() routine
    id = String()

    #: A UI friendly name for the factory. Can contain spaces.
    name = String()

    #: A reference to the plugin that holds this factory.
    plugin = Instance(Plugin)

    def __init__(self, plugin, *args, **kwargs):
        """Initializes the instance.

        Parameters
        ----------
        plugin: Plugin
            The plugin that holds this factory.
        """
        self.plugin = plugin
        super(BaseKPICalculatorFactory, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def create_kpi_calculator(self):
        """Factory method.
        Creates and returns an instance of a KPI Calculator, associated
        to the given application and model.

        Returns
        -------
        BaseKPICalculator
            The specific instance of the generated KPICalculator
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
        BaseKPICalculatorModel
            The model
        """
