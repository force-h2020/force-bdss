import unittest

from force_bdss.core.data_value import DataValue
from force_bdss.core_plugins.dummy.csv_extractor.csv_extractor_data_source \
    import CSVExtractorDataSource
from force_bdss.core_plugins.dummy.csv_extractor.csv_extractor_model import \
    CSVExtractorModel
from force_bdss.data_sources.base_data_source_bundle import \
    BaseDataSourceBundle
from force_bdss.tests import fixtures

try:
    import mock
except ImportError:
    from unittest import mock


class TestCSVExtractorDataSource(unittest.TestCase):
    def setUp(self):
        self.bundle = mock.Mock(spec=BaseDataSourceBundle)

    def test_initialization(self):
        ds = CSVExtractorDataSource(self.bundle)
        self.assertEqual(ds.bundle, self.bundle)

    def test_run(self):
        ds = CSVExtractorDataSource(self.bundle)
        model = CSVExtractorModel(self.bundle)
        model.filename = fixtures.get("foo.csv")
        model.row = 3
        model.column = 5
        mock_params = []
        result = ds.run(model, mock_params)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], DataValue)
        self.assertEqual(result[0].value, 42)
