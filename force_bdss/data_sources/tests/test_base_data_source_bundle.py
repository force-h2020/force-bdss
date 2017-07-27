import unittest
try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin
from force_bdss.data_sources.base_data_source_bundle import \
    BaseDataSourceBundle


class DummyDataSourceBundle(BaseDataSourceBundle):
    id = "foo"

    name = "bar"

    def create_data_source(self):
        pass

    def create_model(self, model_data=None):
        pass


class TestBaseDataSourceBundle(unittest.TestCase):
    def test_initialization(self):
        bundle = DummyDataSourceBundle(mock.Mock(spec=Plugin))
        self.assertEqual(bundle.id, 'foo')
        self.assertEqual(bundle.name, 'bar')
