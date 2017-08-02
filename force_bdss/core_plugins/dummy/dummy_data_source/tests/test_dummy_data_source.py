import unittest

from force_bdss.core_plugins.dummy.dummy_data_source.dummy_data_source import \
    DummyDataSource
from force_bdss.core_plugins.dummy.dummy_data_source.dummy_data_source_model\
    import \
    DummyDataSourceModel
from force_bdss.data_sources.base_data_source_bundle import \
    BaseDataSourceBundle

try:
    import mock
except ImportError:
    from unittest import mock


class TestDummyDataSource(unittest.TestCase):
    def setUp(self):
        self.bundle = mock.Mock(spec=BaseDataSourceBundle)

    def test_initialization(self):
        ds = DummyDataSource(self.bundle)
        self.assertEqual(ds.bundle, self.bundle)

    def test_slots(self):
        ds = DummyDataSource(self.bundle)
        model = DummyDataSourceModel(self.bundle)
        slots = ds.slots(model)
        self.assertEqual(slots, ((), ()))

