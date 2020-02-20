import unittest

from traits.testing.api import UnittestTools

from force_bdss.data_sources.i_data_source_factory import IDataSourceFactory
from force_bdss.tests.dummy_classes.data_source import (
    DummyDataSource,
    DummyDataSourceModel,
)

from unittest import mock


class TestBaseDataSource(unittest.TestCase, UnittestTools):
    def setUp(self):
        self.factory = mock.Mock(spec=IDataSourceFactory)
        self.ds = DummyDataSource(self.factory)
        self.model = DummyDataSourceModel(self.factory)

    def test_initialization(self):
        self.assertEqual(self.ds.factory, self.factory)

    def test__run(self):
        with mock.patch.object(DummyDataSource, "run") as mock_run:
            ds = DummyDataSource(self.factory)
            with self.assertTraitChanges(self.model, "event", count=2):
                ds._run(self.model, [])
        self.assertEqual(1, mock_run.call_count)
