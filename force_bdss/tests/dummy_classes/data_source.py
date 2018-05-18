from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.base_data_source_factory import \
    BaseDataSourceFactory
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel


class DummyDataSource(BaseDataSource):
    def run(self, *args, **kwargs):
        pass

    def slots(self, model):
        return (), ()


class DummyDataSourceModel(BaseDataSourceModel):
    pass


class DummyDataSourceFactory(BaseDataSourceFactory):
    def get_identifier(self):
        return "dummy_data_source"

    def get_name(self):
        return "Dummy data source"

    def get_model_class(self):
        return DummyDataSourceModel

    def get_data_source_class(self):
        return DummyDataSource
