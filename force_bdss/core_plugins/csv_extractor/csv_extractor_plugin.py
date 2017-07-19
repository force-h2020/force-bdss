from force_bdss.api import BaseExtensionPlugin

from .csv_extractor.csv_extractor_bundle import CSVExtractorBundle


class CSVExtractorPlugin(BaseExtensionPlugin):
    def _data_source_bundles_default(self):
        return [CSVExtractorBundle()]
