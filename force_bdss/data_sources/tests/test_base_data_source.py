import unittest

from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel
from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.bdss_application import BDSSApplication


class DummyDataSource(BaseDataSource):
    def run(self, *args, **kwargs):
        pass


class TestBaseDataSource(unittest.TestCase):
    def test_initialization(self):
        bundle = mock.Mock(spec=IDataSourceBundle)
        application = mock.Mock(spec=BDSSApplication)
        model = mock.Mock(spec=BaseDataSourceModel)
        ds = DummyDataSource(bundle, application, model)

        self.assertEqual(ds.bundle, bundle)
        self.assertEqual(ds.application, application)
        self.assertEqual(ds.model, model)
