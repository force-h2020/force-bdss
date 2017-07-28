from traits.api import Interface, String, Instance
from envisage.plugin import Plugin


class IMCOBundle(Interface):
    """Interface for the BaseMCOBundle.
    You should not need it, as its main use is for envisage support.

    Refer to BaseMCOBundle for documentation
    """
    id = String()

    name = String()

    plugin = Instance(Plugin)

    def create_optimizer(self):
        """"""

    def create_model(self, model_data=None):
        """"""

    def create_communicator(self):
        """"""
