import unittest

from force_bdss.data_sources.i_data_source_factory import IDataSourceFactory
from force_bdss.tests.dummy_classes.data_source import DummyDataSource

try:
    import mock
except ImportError:
    from unittest import mock


class TestBaseDataSource(unittest.TestCase):
    def test_initialization(self):
        factory = mock.Mock(spec=IDataSourceFactory)
        ds = DummyDataSource(factory)

        self.assertEqual(ds.factory, factory)
