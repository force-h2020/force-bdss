from traits.api import Type

from force_bdss.core.i_factory import IFactory


class IMCOFactory(IFactory):
    """Interface for the BaseMCOFactory.
    You should not need it, as its main use is for envisage support.

    Refer to BaseMCOFactory for documentation
    """
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

    def get_model_class(self):
        pass

    def get_communicator_class(self):
        pass

    def get_optimizer_class(self):
        pass

    def create_optimizer(self):
        pass

    def create_model(self):
        pass

    def create_communicator(self):
        pass

    def parameter_factories(self):
        pass
