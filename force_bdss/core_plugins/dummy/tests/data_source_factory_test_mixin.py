from envisage.plugin import Plugin

try:
    import mock
except ImportError:
    from unittest import mock


class DataSourceFactoryTestMixin(object):
    def setUp(self):
        self.plugin = mock.Mock(spec=Plugin)
        super(DataSourceFactoryTestMixin, self).setUp()

    # Note: we can't use metaclasses. Apparently using six.with_metaclass
    # breaks the unittest TestCase mechanism. py3 metaclassing works.
    @property
    def factory_class(self):
        raise NotImplementedError()

    @property
    def model_class(self):
        raise NotImplementedError()

    @property
    def data_source_class(self):
        raise NotImplementedError()

    def test_initialization(self):
        factory = self.factory_class(self.plugin)
        self.assertNotEqual(factory.id, "")
        self.assertEqual(factory.plugin, self.plugin)

    def test_create_model(self):
        factory = self.factory_class(self.plugin)
        model = factory.create_model({})
        self.assertIsInstance(model, self.model_class)

        model = factory.create_model()
        self.assertIsInstance(model, self.model_class)

    def test_create_data_source(self):
        factory = self.factory_class(self.plugin)
        ds = factory.create_data_source()
        self.assertIsInstance(ds, self.data_source_class)
