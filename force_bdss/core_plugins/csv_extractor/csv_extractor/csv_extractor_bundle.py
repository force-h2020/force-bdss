from traits.api import provides, HasStrictTraits
from traits.trait_types import String

from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle

from .csv_extractor_model import CSVExtractorModel
from .csv_extractor_data_source import CSVExtractorDataSource


@provides(IDataSourceBundle)
class CSVExtractorBundle(HasStrictTraits):
    name = String("csv_extractor")

    def create_model(self, model_data):
        return CSVExtractorModel.from_json(model_data)

    def create_ui(self, model):
        pass

    def create_data_source(self, application, model):
        return CSVExtractorDataSource(self, application, model)
