from envisage.api import Plugin
from traits.api import Interface, String, Instance

from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel


class IDataSourceFactory(Interface):
    """Envisage required interface for the BaseDataSourceFactory.
    You should not need to use this directly.

    Refer to the BaseDataSourceFactory for documentation.
    """
    id = String()

    name = String()

    data_source_class = Instance(BaseDataSource)

    model_class = Instance(BaseDataSourceModel)

    plugin = Instance(Plugin)

    def create_data_source(self):
        """"""

    def create_model(self, model_data=None):
        """"""
