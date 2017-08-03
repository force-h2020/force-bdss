import unittest

from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle

try:
    import mock
except ImportError:
    from unittest import mock


class DummyDataSource(BaseDataSource):
    def run(self, *args, **kwargs):
        pass

    def slots(self, model):
        return (), ()


class TestBaseDataSource(unittest.TestCase):
    def test_initialization(self):
        bundle = mock.Mock(spec=IDataSourceBundle)
        ds = DummyDataSource(bundle)

        self.assertEqual(ds.bundle, bundle)
