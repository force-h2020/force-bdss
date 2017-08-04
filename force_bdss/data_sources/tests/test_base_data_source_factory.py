import unittest
try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin
from force_bdss.data_sources.base_data_source_factory import \
    BaseDataSourceFactory


class DummyDataSourceFactory(BaseDataSourceFactory):
    id = "foo"

    name = "bar"

    def create_data_source(self):
        pass

    def create_model(self, model_data=None):
        pass


class TestBaseDataSourceFactory(unittest.TestCase):
    def test_initialization(self):
        factory = DummyDataSourceFactory(mock.Mock(spec=Plugin))
        self.assertEqual(factory.id, 'foo')
        self.assertEqual(factory.name, 'bar')
