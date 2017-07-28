import unittest

from force_bdss.data_sources.base_data_source_bundle import \
    BaseDataSourceBundle
from force_bdss.data_sources.tests.test_base_data_source import DummyDataSource

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
