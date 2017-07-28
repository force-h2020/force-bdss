import unittest

from force_bdss.core_plugins.dummy.tests.data_source_bundle_test_mixin import \
    DataSourceBundleTestMixin
from force_bdss.core_plugins.dummy.csv_extractor.csv_extractor_bundle import \
    CSVExtractorBundle
from force_bdss.core_plugins.dummy.csv_extractor.csv_extractor_data_source \
    import CSVExtractorDataSource
from force_bdss.core_plugins.dummy.csv_extractor.csv_extractor_model import \
    CSVExtractorModel


class TestCSVExtractorBundle(DataSourceBundleTestMixin, unittest.TestCase):
    @property
    def bundle_class(self):
        return CSVExtractorBundle

    @property
    def model_class(self):
        return CSVExtractorModel

    @property
    def data_source_class(self):
        return CSVExtractorDataSource
