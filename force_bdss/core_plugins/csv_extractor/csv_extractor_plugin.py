from envisage.plugin import Plugin
from traits.api import List

from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle

from .csv_extractor.csv_extractor_bundle import CSVExtractorBundle


class CSVExtractorPlugin(Plugin):
    id = "force.bdss.data_sources.csv_extractor"

    data_sources = List(
        IDataSourceBundle,
        contributes_to='force.bdss.data_sources.bundles'
    )

    def _data_sources_default(self):
        return [CSVExtractorBundle()]
