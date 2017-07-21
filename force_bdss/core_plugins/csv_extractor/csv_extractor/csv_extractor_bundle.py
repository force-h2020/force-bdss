from traits.api import String

from force_bdss.api import bundle_id, BaseDataSourceBundle

from .csv_extractor_model import CSVExtractorModel
from .csv_extractor_data_source import CSVExtractorDataSource


class CSVExtractorBundle(BaseDataSourceBundle):
    id = String(bundle_id("enthought", "csv_extractor"))

    name = String("CSV Extractor")

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}

        return CSVExtractorModel(self, **model_data)

    def create_data_source(self, application, model):
        return CSVExtractorDataSource(self, application, model)
