from traits.api import Interface, String, Instance, Type
from envisage.plugin import Plugin


class IMCOFactory(Interface):
    """Interface for the BaseMCOFactory.
    You should not need it, as its main use is for envisage support.

    Refer to BaseMCOFactory for documentation
    """
    id = String()

    name = String()

    optimizer_class = Type(
        "force_bdss.mco.base_mco.BaseMCO"
    )

    model_class = Type(
        "force_bdss.mco.base_mco_communicator.BaseMCOCommunicator"
    )

    communicator_class = Type(
        "force_bdss.mco.base_mco_model.BaseMCOModel"
    )

    plugin = Instance(Plugin)

    def create_optimizer(self):
        """"""

    def create_model(self, model_data=None):
        """"""

    def create_communicator(self):
        """"""
