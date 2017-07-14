from traits.api import provides, HasStrictTraits, String

from force_bdss.data_sources.basic_data_source import BasicDataSource
from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle
from force_bdss.mco.basic_model import BasicModel


@provides(IDataSourceBundle)
class BasicBundle(HasStrictTraits):
    name = String("basic")

    def create_model(self, model_data):
        return BasicModel.from_json(model_data)

    def create_ui(self):
        pass

    def create_data_source(self, application, model):
        return BasicDataSource(self, application, model)
