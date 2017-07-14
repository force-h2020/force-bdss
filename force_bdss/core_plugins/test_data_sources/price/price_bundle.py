from traits.api import provides, HasStrictTraits
from traits.trait_types import String

from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle

from .price_model import PriceModel
from .price_data_source import PriceDataSource


@provides(IDataSourceBundle)
class PriceBundle(HasStrictTraits):
    name = String("price")

    def create_model(self, model_data):
        return PriceModel.from_json(model_data)

    def create_ui(self):
        pass

    def create_data_source(self, application, model):
        return PriceDataSource(self, application, model)
