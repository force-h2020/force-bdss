from traits.api import provides, HasStrictTraits
from traits.trait_types import String

from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle
from force_bdss.id_generators import bundle_id

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
