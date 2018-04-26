import unittest

from force_bdss.data_sources.tests.test_base_data_source import DummyDataSource
from force_bdss.data_sources.tests.test_base_data_source_model import \
    DummyDataSourceModel

try:
    import mock
except ImportError:
    from unittest import mock

import testfixtures

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


class DummyDataSourceFactoryFast(BaseDataSourceFactory):
    id = "foo"

    name = "bar"

    model_class = DummyDataSourceModel

    data_source_class = DummyDataSource


class TestBaseDataSourceFactory(unittest.TestCase):
    def test_initialization(self):
        factory = DummyDataSourceFactory(mock.Mock(spec=Plugin))
        self.assertEqual(factory.id, 'foo')
        self.assertEqual(factory.name, 'bar')

    def test_fast_specification(self):
        factory = DummyDataSourceFactoryFast(mock.Mock(spec=Plugin))
        self.assertIsInstance(factory.create_data_source(), DummyDataSource)
        self.assertIsInstance(factory.create_model(), DummyDataSourceModel)

    def test_fast_specification_errors(self):
        factory = DummyDataSourceFactoryFast(mock.Mock(spec=Plugin))
        factory.model_class = None
        factory.data_source_class = None

        with testfixtures.LogCapture():
            with self.assertRaises(RuntimeError):
                factory.create_data_source()

            with self.assertRaises(RuntimeError):
                factory.create_model()
