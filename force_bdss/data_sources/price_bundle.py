from traits.api import provides, HasStrictTraits

from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle
from force_bdss.data_sources.price_data_source import PriceDataSource
from force_bdss.data_sources.price_model import PriceModel


@provides(IDataSourceBundle)
class PriceBundle(HasStrictTraits):
    def create_model(self, model_data):
        return PriceModel.from_json(model_data)

    def create_ui(self):
        pass

    def create_data_source(self, application, model):
        return PriceDataSource(self, application, model)
