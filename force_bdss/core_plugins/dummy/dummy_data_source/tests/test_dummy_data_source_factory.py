import unittest

from force_bdss.core_plugins.dummy.dummy_data_source.dummy_data_source import \
    DummyDataSource
from force_bdss.core_plugins.dummy.dummy_data_source\
    .dummy_data_source_factory import DummyDataSourceFactory
from force_bdss.core_plugins.dummy.dummy_data_source.dummy_data_source_model\
    import DummyDataSourceModel
from force_bdss.core_plugins.dummy.tests.data_source_factory_test_mixin \
    import DataSourceFactoryTestMixin


class TestDummyDataSourceFactory(
        DataSourceFactoryTestMixin, unittest.TestCase):
    @property
    def factory_class(self):
        return DummyDataSourceFactory

    @property
    def model_class(self):
        return DummyDataSourceModel

    @property
    def data_source_class(self):
        return DummyDataSource
