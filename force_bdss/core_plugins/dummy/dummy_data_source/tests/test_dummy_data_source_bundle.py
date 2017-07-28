import unittest

from force_bdss.core_plugins.dummy.dummy_data_source.dummy_data_source import \
    DummyDataSource
from force_bdss.core_plugins.dummy.dummy_data_source\
    .dummy_data_source_bundle import DummyDataSourceBundle
from force_bdss.core_plugins.dummy.dummy_data_source.dummy_data_source_model\
    import DummyDataSourceModel
from force_bdss.core_plugins.dummy.tests.data_source_bundle_test_mixin import \
    DataSourceBundleTestMixin


class TestDummyDataSourceBundle(DataSourceBundleTestMixin, unittest.TestCase):
    @property
    def bundle_class(self):
        return DummyDataSourceBundle

    @property
    def model_class(self):
        return DummyDataSourceModel

    @property
    def data_source_class(self):
        return DummyDataSource
