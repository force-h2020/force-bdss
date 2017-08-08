from force_bdss.api import BaseDataSourceFactory, factory_id
from .dummy_data_source_model import DummyDataSourceModel
from .dummy_data_source import DummyDataSource


class DummyDataSourceFactory(BaseDataSourceFactory):
    id = factory_id("enthought", "dummy_data_source")

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}

        return DummyDataSourceModel(self, **model_data)

    def create_data_source(self):
        return DummyDataSource(self)
