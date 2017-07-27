import abc

from traits.api import ABCHasStrictTraits, String, provides, Instance
from envisage.plugin import Plugin

from .i_mco_bundle import IMCOBundle


@provides(IMCOBundle)
class BaseMCOBundle(ABCHasStrictTraits):
    """Base class for the MultiCriteria Optimizer bundle.
    """
    # NOTE: any changes to the interface of this class must be replicated
    # in the IMultiCriteriaOptimizerBundle interface class.

    #: A unique ID produced with the bundle_id() routine.
    id = String()

    #: A user friendly name of the bundle. Spaces allowed.
    name = String()

    plugin = Instance(Plugin)

    def __init__(self, plugin, *args, **kwargs):
        self.plugin = plugin
        super(BaseMCOBundle, self).__init__(*args, **kwargs)

    @abc.abstractmethod
    def create_optimizer(self):
        """Factory method.
        Creates the optimizer with the given application
        and model and returns it to the caller.

        Parameters
        ----------
        application: Application
            The envisage application instance
        model: BaseMCOModel
            The model to associate to the optimizer, instantiated through
            create_model()

        Returns
        -------
        BaseMCOOptimizer
            The optimizer
        """

    @abc.abstractmethod
    def create_model(self, model_data=None):
        """Factory method.
        Creates the model object (or network of model objects) of the MCO.
        The model can provide a traits UI View according to traitsui
        specifications, so that a UI can be provided automatically.

        Parameters
        ----------
        model_data: dict or None
            A dictionary of data that can be interpreted appropriately to
            recreate the model. If None, an empty (with defaults) model will
            be created and returned.

        Returns
        -------
        BaseMCOModel
            The MCOModel
        """

    @abc.abstractmethod
    def create_communicator(self):
        """Factory method. Returns the communicator class that allows
        exchange between the MCO and the evaluator code.

        Parameters
        ----------
        application: Application
            The envisage application instance
        model: BaseMCOModel
            The model to associate to the optimizer, instantiated through
            create_model()
        """
