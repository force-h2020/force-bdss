import logging
from traits.api import ABCHasStrictTraits, Str, provides, Instance, Type
from envisage.plugin import Plugin

from force_bdss.ids import factory_id
from force_bdss.mco.base_mco import BaseMCO
from force_bdss.mco.base_mco_communicator import BaseMCOCommunicator
from force_bdss.mco.base_mco_model import BaseMCOModel
from .i_mco_factory import IMCOFactory

log = logging.getLogger(__name__)


@provides(IMCOFactory)
class BaseMCOFactory(ABCHasStrictTraits):
    """Base class for the MultiCriteria Optimizer factory.
    """
    # NOTE: any changes to the interface of this class must be replicated
    # in the IMultiCriteriaOptimizerFactory interface class.

    #: A unique ID produced with the factory_id() routine.
    id = Str()

    #: A user friendly name of the factory. Spaces allowed.
    name = Str()

    #: The optimizer class to instantiate. Define this to your MCO class.
    optimizer_class = Type(BaseMCO, allow_none=False)

    #: The model associated to the MCO. Define this to your MCO model class.
    model_class = Type(BaseMCOModel, allow_none=False)

    #: The communicator associated to the MCO. Define this to your MCO comm.
    communicator_class = Type(BaseMCOCommunicator, allow_none=False)

    #: A reference to the Plugin that holds this factory.
    plugin = Instance(Plugin, allow_none=False)

    def __init__(self, plugin, *args, **kwargs):
        self.plugin = plugin
        super(BaseMCOFactory, self).__init__(*args, **kwargs)

        self.name = self.get_name()
        self.optimizer_class = self.get_optimizer_class()
        self.model_class = self.get_model_class()
        self.communicator_class = self.get_communicator_class()
        identifier = self.get_identifier()
        try:
            id = factory_id(self.plugin.id, identifier)
        except ValueError:
            raise ValueError(
                "Invalid identifier {} returned by "
                "{}.get_identifier()".format(
                    identifier,
                    self.__class__.__name__
                )
            )
        self.id = id

    def get_optimizer_class(self):
        raise NotImplementedError(
            "get_optimizer_class was not implemented in factory {}".format(
                self.__class__))

    def get_model_class(self):
        raise NotImplementedError(
            "get_model_class was not implemented in factory {}".format(
                self.__class__))

    def get_communicator_class(self):
        raise NotImplementedError(
            "get_communicator_class was not implemented in factory {}".format(
                self.__class__))

    def get_identifier(self):
        raise NotImplementedError(
            "get_identifier was not implemented in factory {}".format(
                self.__class__))

    def get_name(self):
        raise NotImplementedError(
            "get_name was not implemented in factory {}".format(
                self.__class__))

    def create_optimizer(self):
        """Factory method.
        Creates the optimizer with the given application
        and model and returns it to the caller.

        Returns
        -------
        BaseMCO
            The optimizer
        """
        if self.optimizer_class is None:
            msg = ("optimizer_class cannot be None in {}. Either define "
                   "optimizer_class or reimplement create_optimizer on "
                   "your factory class.".format(self.__class__.__name__))
            log.error(msg)
            raise RuntimeError(msg)

        return self.optimizer_class(self)

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
        if model_data is None:
            model_data = {}

        if self.model_class is None:
            msg = ("model_class cannot be None in {}. Either define "
                   "model_class or reimplement create_model on your "
                   "factory class.".format(self.__class__.__name__))
            log.error(msg)
            raise RuntimeError(msg)

        return self.model_class(self, **model_data)

    def create_communicator(self):
        """Factory method. Returns the communicator class that allows
        exchange between the MCO and the evaluator code.

        Returns
        -------
        BaseMCOCommunicator
            An instance of the communicator
        """
        if self.communicator_class is None:
            msg = ("communicator_class cannot be None in {}. Either define "
                   "communicator_class or reimplement create_communicator on "
                   "your factory class.".format(self.__class__.__name__))
            log.error(msg)
            raise RuntimeError(msg)

        return self.communicator_class(self)

    def parameter_factories(self):
        """Returns the parameter factories supported by this MCO

        Returns
        -------
        List of BaseMCOParameterFactory
        """
