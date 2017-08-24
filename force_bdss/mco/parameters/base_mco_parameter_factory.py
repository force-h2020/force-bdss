from traits.api import HasStrictTraits, String, Type, Instance

from ..base_mco_factory import BaseMCOFactory


class BaseMCOParameterFactory(HasStrictTraits):
    """Factory that produces the model instance of a given BASEMCOParameter
    instance.

    Must be reimplemented for the specific parameter. The generic create_model
    is generally enough, and the only entity to define is model_class with
    the appropriate class of the parameter.
    """

    #: A reference to the MCO factory this parameter factory lives in.
    mco_factory = Instance(BaseMCOFactory)

    #: A unique string identifying the parameter
    id = String()

    #: A user friendly name (for the UI)
    name = String("Undefined parameter")

    #: A long description of the parameter
    description = String("Undefined parameter")

    # The model class to instantiate when create_model is called.
    model_class = Type('BaseMCOParameter')

    def __init__(self, mco_factory, *args, **kwargs):
        self.mco_factory = mco_factory
        super(BaseMCOParameterFactory, self).__init__(*args, **kwargs)

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
