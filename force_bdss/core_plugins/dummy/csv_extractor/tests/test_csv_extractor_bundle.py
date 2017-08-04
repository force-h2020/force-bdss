import unittest

from force_bdss.core_plugins.dummy.tests.data_source_factory_test_mixin import \
    DataSourceFactoryTestMixin
from force_bdss.core_plugins.dummy.csv_extractor.csv_extractor_factory import \
    CSVExtractorFactory
from force_bdss.core_plugins.dummy.csv_extractor.csv_extractor_data_source \
    import CSVExtractorDataSource
from force_bdss.core_plugins.dummy.csv_extractor.csv_extractor_model import \
    CSVExtractorModel


class TestCSVExtractorBundle(DataSourceFactoryTestMixin, unittest.TestCase):
    @property
    def factory_class(self):
        return CSVExtractorFactory

    @property
    def model_class(self):
        return CSVExtractorModel

    @property
    def data_source_class(self):
        return CSVExtractorDataSource
