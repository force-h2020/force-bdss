from traits.api import Interface, String, Instance
from envisage.plugin import Plugin


class IMCOBundle(Interface):
    """Interface for the MultiCriteria Optimizer bundle.
    You should not need it, as its main use is for envisage support.
    """
    id = String()

    name = String()

    plugin = Instance(Plugin)

    def create_optimizer(self):
        pass

    def create_model(self, model_data=None):
        pass

    def create_communicator(self):
        pass
