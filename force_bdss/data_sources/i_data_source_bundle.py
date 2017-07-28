from envisage.api import Plugin
from traits.api import Interface, String, Instance


class IDataSourceBundle(Interface):
    """Envisage required interface for the BaseDataSourceBundle.
    You should not need to use this directly.

    Refer to the BaseDataSourceBundle for documentation.
    """
    id = String()

    name = String()

    plugin = Instance(Plugin)

    def create_data_source(self):
        """"""

    def create_model(self, model_data=None):
        """"""
