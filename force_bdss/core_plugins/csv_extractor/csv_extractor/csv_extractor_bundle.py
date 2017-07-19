from traits.api import provides, HasStrictTraits, String

from force_bdss.api import bundle_id, IDataSourceBundle

from .csv_extractor_model import CSVExtractorModel
from .csv_extractor_data_source import CSVExtractorDataSource


@provides(IDataSourceBundle)
class CSVExtractorBundle(HasStrictTraits):
    id = String(bundle_id("enthought", "csv_extractor"))

    def create_model(self, model_data=None):
        if model_data is None:
            return CSVExtractorModel()
        else:
            return CSVExtractorModel.from_json(model_data)

    def create_data_source(self, application, model):
        return CSVExtractorDataSource(self, application, model)
