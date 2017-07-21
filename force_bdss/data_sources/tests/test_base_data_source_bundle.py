import unittest

from force_bdss.data_sources.base_data_source_bundle import \
    BaseDataSourceBundle


class DummyDataSourceBundle(BaseDataSourceBundle):
    id = "foo"

    name = "bar"

    def create_data_source(self, application, model):
        pass

    def create_model(self, model_data=None):
        pass


class TestBaseDataSourceBundle(unittest.TestCase):
    def test_initialization(self):
        bundle = DummyDataSourceBundle()
        self.assertEqual(bundle.id, 'foo')
        self.assertEqual(bundle.name, 'bar')
