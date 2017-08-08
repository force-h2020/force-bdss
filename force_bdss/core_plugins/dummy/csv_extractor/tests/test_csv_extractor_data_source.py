import unittest

from force_bdss.core.data_value import DataValue
from force_bdss.core.slot import Slot
from force_bdss.core_plugins.dummy.csv_extractor.csv_extractor_data_source \
    import CSVExtractorDataSource
from force_bdss.core_plugins.dummy.csv_extractor.csv_extractor_model import \
    CSVExtractorModel
from force_bdss.data_sources.base_data_source_factory import \
    BaseDataSourceFactory
from force_bdss.tests import fixtures

try:
    import mock
except ImportError:
    from unittest import mock


class TestCSVExtractorDataSource(unittest.TestCase):
    def setUp(self):
        self.factory = mock.Mock(spec=BaseDataSourceFactory)

    def test_initialization(self):
        ds = CSVExtractorDataSource(self.factory)
        self.assertEqual(ds.factory, self.factory)

    def test_run(self):
        ds = CSVExtractorDataSource(self.factory)
        model = CSVExtractorModel(self.factory)
        model.filename = fixtures.get("foo.csv")
        model.row = 3
        model.column = 5
        mock_params = []
        result = ds.run(model, mock_params)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], DataValue)
        self.assertEqual(result[0].value, 42)

    def test_run_with_exception(self):
        ds = CSVExtractorDataSource(self.factory)
        model = CSVExtractorModel(self.factory)
        model.filename = fixtures.get("foo.csv")
        mock_params = []
        model.row = 30
        model.column = 5
        with self.assertRaises(IndexError):
            ds.run(model, mock_params)

        model.row = 3
        model.column = 50
        with self.assertRaises(IndexError):
            ds.run(model, mock_params)

    def test_slots(self):
        ds = CSVExtractorDataSource(self.factory)
        model = CSVExtractorModel(self.factory)
        slots = ds.slots(model)
        self.assertEqual(len(slots), 2)
        self.assertEqual(len(slots[0]), 0)
        self.assertEqual(len(slots[1]), 1)
        self.assertIsInstance(slots[1][0], Slot)
