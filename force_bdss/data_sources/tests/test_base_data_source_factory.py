from unittest import TestCase
import testfixtures

from traits.trait_errors import TraitError

from force_bdss.data_sources.tests.test_base_data_source import \
    DummyDataSource
from force_bdss.data_sources.tests.test_base_data_source_model import \
    DummyDataSourceModel
from force_bdss.tests.dummy_classes.data_source import DummyDataSourceFactory


class TestBaseDataSourceFactory(TestCase):
    def setUp(self):
        self.plugin = {'id': "pid", 'name': 'Plugin'}

    def test_initialization(self):
        factory = DummyDataSourceFactory(self.plugin)
        self.assertEqual(factory.id, 'pid.factory.dummy_data_source')
        self.assertEqual(factory.plugin_id, 'pid')
        self.assertEqual(factory.name, 'Dummy data source')
        self.assertEqual(factory.description, "No description available.")
        self.assertEqual(factory.model_class, DummyDataSourceModel)
        self.assertEqual(factory.data_source_class, DummyDataSource)
        self.assertIsInstance(factory.create_data_source(), DummyDataSource)
        self.assertIsInstance(factory.create_model(), DummyDataSourceModel)

    def test_initialization_errors_invalid_idetifier(self):
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

    def test_exception_create_data_source(self):

        class BrokenDataSource(DummyDataSource):
            def __init__(self, *args, **kawrgs):
                super().__init__(*args, **kawrgs)
                raise RuntimeError

        class BrokenFactory(DummyDataSourceFactory):
            def get_data_source_class(self):
                return BrokenDataSource

        factory = BrokenFactory(self.plugin)

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(RuntimeError):
                factory.create_data_source()
            capture.check(
                ('force_bdss.data_sources.base_data_source_factory',
                 'ERROR',
                 'Unable to create DataSource from factory pid.factory'
                 '.dummy_data_source in '
                 'plugin pid. This may indicate a programming error in'
                 ' the plugin')
            )

    def test_exception_create_model(self):

        class BrokenDataSourceModel(DummyDataSourceModel):
            def __init__(self, *args, **kawrgs):
                super().__init__(*args, **kawrgs)
                raise RuntimeError

        class BrokenFactory(DummyDataSourceFactory):
            def get_model_class(self):
                return BrokenDataSourceModel

        factory = BrokenFactory(self.plugin)

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(RuntimeError):
                factory.create_model()
            capture.check(
                ('force_bdss.data_sources.base_data_source_factory',
                 'ERROR',
                 'Unable to create DataSourceModel from factory '
                 'pid.factory.dummy_data_source in '
                 'plugin pid. This may indicate a programming error in'
                 ' the plugin')
            )
