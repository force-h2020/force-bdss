from traits.api import String

from force_bdss.api import factory_id, BaseDataSourceFactory

from .csv_extractor_model import CSVExtractorModel
from .csv_extractor_data_source import CSVExtractorDataSource


class CSVExtractorFactory(BaseDataSourceFactory):
    id = String(factory_id("enthought", "csv_extractor"))

    name = String("CSV Extractor")

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}

        return CSVExtractorModel(self, **model_data)

    def create_data_source(self):
        return CSVExtractorDataSource(self)
