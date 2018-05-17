from traits.api import HasStrictTraits, Str, Type, Instance

from force_bdss.ids import mco_parameter_id


class BaseMCOParameterFactory(HasStrictTraits):
    """Factory that produces the model instance of a given BASEMCOParameter
    instance.

    Must be reimplemented for the specific parameter. The generic create_model
    is generally enough, and the only entity to define is model_class with
    the appropriate class of the parameter.
    """

    #: A reference to the MCO factory this parameter factory lives in.
    mco_factory = Instance('force_bdss.mco.base_mco_factory.BaseMCOFactory',
                           allow_none=False)

    #: A unique string identifying the parameter
    id = Str()

    #: A user friendly name (for the UI)
    name = Str()

    #: A long description of the parameter
    description = Str()

    # The model class to instantiate when create_model is called.
    model_class = Type(
        "force_bdss.mco.parameters.base_mco_parameter.BaseMCOParameter",
        allow_none=False
    )

    def get_identifier(self):
        raise NotImplementedError(
            "get_identifier was not implemented in factory {}".format(
                self.__class__))

    def get_name(self):
        raise NotImplementedError(
            "get_name was not implemented in factory {}".format(
                self.__class__))

    def get_description(self):
        raise NotImplementedError(
            "get_description was not implemented in factory {}".format(
                self.__class__))

    def get_model_class(self):
        raise NotImplementedError(
            "get_model_class was not implemented in factory {}".format(
                self.__class__))

    def __init__(self, mco_factory, *args, **kwargs):
        self.mco_factory = mco_factory
        super(BaseMCOParameterFactory, self).__init__(*args, **kwargs)

        self.name = self.get_name()
        self.description = self.get_description()
        self.model_class = self.get_model_class()
        identifier = self.get_identifier()
        try:
            id = mco_parameter_id(self.mco_factory.id, identifier)
        except ValueError:
            raise ValueError(
                "Invalid identifier {} returned by "
                "{}.get_identifier()".format(
                    identifier,
                    self.__class__.__name__
                )
            )
        self.id = id

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
