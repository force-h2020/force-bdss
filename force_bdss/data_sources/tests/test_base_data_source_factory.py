import unittest

from traits.trait_errors import TraitError

from force_bdss.data_sources.tests.test_base_data_source import DummyDataSource
from force_bdss.data_sources.tests.test_base_data_source_model import \
    DummyDataSourceModel
from force_bdss.tests.dummy_classes.data_source import DummyDataSourceFactory

try:
    import mock
except ImportError:
    from unittest import mock

import testfixtures

from envisage.plugin import Plugin


class TestBaseDataSourceFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = mock.Mock(spec=Plugin, id="pid")

    def test_initialization(self):
        factory = DummyDataSourceFactory(self.plugin)
        self.assertEqual(factory.id, 'pid.factory.foo')
        self.assertEqual(factory.name, 'bar')
        self.assertEqual(factory.model_class, DummyDataSourceModel)
        self.assertEqual(factory.data_source_class, DummyDataSource)
        self.assertIsInstance(factory.create_data_source(), DummyDataSource)
        self.assertIsInstance(factory.create_model(), DummyDataSourceModel)

    def test_initialization_errors_invalid_identifier(self):
        class Broken(DummyDataSourceFactory):
            def get_identifier(self):
                return None

        with testfixtures.LogCapture():
            with self.assertRaises(ValueError):
                Broken(self.plugin)

    def test_initialization_errors_invalid_name(self):
        class Broken(DummyDataSourceFactory):
            def get_name(self):
                return None

        with testfixtures.LogCapture():
            with self.assertRaises(TraitError):
                Broken(self.plugin)

    def test_initialization_errors_invalid_model_class(self):
        class Broken(DummyDataSourceFactory):
            def get_model_class(self):
                return None

        with testfixtures.LogCapture():
            with self.assertRaises(TraitError):
                Broken(self.plugin)

    def test_initialization_errors_invalid_data_source_class(self):
        class Broken(DummyDataSourceFactory):
            def get_data_source_class(self):
                return None

        with testfixtures.LogCapture():
            with self.assertRaises(TraitError):
                Broken(self.plugin)
