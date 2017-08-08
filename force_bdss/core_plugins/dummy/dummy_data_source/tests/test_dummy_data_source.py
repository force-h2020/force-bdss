import unittest

from force_bdss.core_plugins.dummy.dummy_data_source.dummy_data_source import \
    DummyDataSource
from force_bdss.core_plugins.dummy.dummy_data_source.dummy_data_source_model\
    import \
    DummyDataSourceModel
from force_bdss.data_sources.base_data_source_factory import \
    BaseDataSourceFactory

try:
    import mock
except ImportError:
    from unittest import mock


class TestDummyDataSource(unittest.TestCase):
    def setUp(self):
        self.factory = mock.Mock(spec=BaseDataSourceFactory)

    def test_initialization(self):
        ds = DummyDataSource(self.factory)
        self.assertEqual(ds.factory, self.factory)

    def test_slots(self):
        ds = DummyDataSource(self.factory)
        model = DummyDataSourceModel(self.factory)
        slots = ds.slots(model)
        self.assertEqual(slots, ((), ()))
