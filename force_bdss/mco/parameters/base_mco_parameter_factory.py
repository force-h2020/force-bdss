from traits.api import Str, Type, Instance, provides

from force_bdss.core.base_factory import BaseFactory
from force_bdss.ids import mco_parameter_id
from force_bdss.mco.parameters.i_mco_parameter_factory import \
    IMCOParameterFactory


@provides(IMCOParameterFactory)
class BaseMCOParameterFactory(BaseFactory):
    """Factory that produces the model instance of a given BASEMCOParameter
    instance.

    Must be reimplemented for the specific parameter. The generic create_model
    is generally enough, and the only entity to define is model_class with
    the appropriate class of the parameter.
    """

    #: A reference to the MCO factory this parameter factory lives in.
    mco_factory = Instance('force_bdss.mco.base_mco_factory.BaseMCOFactory',
                           allow_none=False)

    #: A long description of the parameter
    description = Str()

    # The model class to instantiate when create_model is called.
    model_class = Type(
        "force_bdss.mco.parameters.base_mco_parameter.BaseMCOParameter",
        allow_none=False
    )

    def get_description(self):
        raise NotImplementedError(
            "get_description was not implemented in factory {}".format(
                self.__class__))

    def get_model_class(self):
        raise NotImplementedError(
            "get_model_class was not implemented in factory {}".format(
                self.__class__))

    def __init__(self, mco_factory):
        self.mco_factory = mco_factory
        super(BaseMCOParameterFactory, self).__init__(
            plugin=mco_factory.plugin)

        self.description = self.get_description()
        self.model_class = self.get_model_class()

    def create_model(self, data_values=None):
        """Creates the instance of the model class and returns it.
        You should not reimplement this, as the default is generally ok.
        Instead, just define model_class with the appropriate Parameter class.

        Parameters
        ----------
        data_values: dict or None
            The dictionary of values for this parameter. If None, a default
            object will be returned.

        Returns
        -------
        instance of model_class.
        """
        if data_values is None:
            data_values = {}

        return self.model_class(factory=self, **data_values)

    def _global_id(self, identifier):
        return mco_parameter_id(self.mco_factory.id, identifier)
