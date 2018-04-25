from traits.api import Interface, String, Instance
from envisage.plugin import Plugin

from force_bdss.mco.base_mco import BaseMCO
from force_bdss.mco.base_mco_communicator import BaseMCOCommunicator
from force_bdss.mco.base_mco_model import BaseMCOModel


class IMCOFactory(Interface):
    """Interface for the BaseMCOFactory.
    You should not need it, as its main use is for envisage support.

    Refer to BaseMCOFactory for documentation
    """
    id = String()

    name = String()

    optimizer_class = Instance(BaseMCO)

    model_class = Instance(BaseMCOModel)

    communicator_class = Instance(BaseMCOCommunicator)

    plugin = Instance(Plugin)

    def create_optimizer(self):
        """"""

    def create_model(self, model_data=None):
        """"""

    def create_communicator(self):
        """"""
