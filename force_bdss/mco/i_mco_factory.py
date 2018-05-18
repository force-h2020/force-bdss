from traits.api import Interface, Str, Instance, Type
from envisage.plugin import Plugin


class IMCOFactory(Interface):
    """Interface for the BaseMCOFactory.
    You should not need it, as its main use is for envisage support.

    Refer to BaseMCOFactory for documentation
    """
    id = Str()

    name = Str()

    optimizer_class = Type(
        "force_bdss.mco.base_mco.BaseMCO",
        allow_none=False
    )

    model_class = Type(
        "force_bdss.mco.base_mco_communicator.BaseMCOCommunicator",
        allow_none=False

    )

    communicator_class = Type(
        "force_bdss.mco.base_mco_model.BaseMCOModel",
        allow_none=False
    )

    plugin = Instance(Plugin, allow_none=False)

    def get_model_class(self):
        pass

    def get_communicator_class(self):
        pass

    def get_optimizer_class(self):
        pass

    def get_identifier(self):
        pass

    def get_name(self):
        pass

    def create_optimizer(self):
        pass

    def create_model(self):
        pass

    def create_communicator(self):
        pass

    def parameter_factories(self):
        pass
