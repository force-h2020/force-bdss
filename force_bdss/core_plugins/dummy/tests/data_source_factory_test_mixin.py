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
        bundle = self.factory_class(self.plugin)
        self.assertNotEqual(bundle.id, "")
        self.assertEqual(bundle.plugin, self.plugin)

    def test_create_model(self):
        bundle = self.factory_class(self.plugin)
        model = bundle.create_model({})
        self.assertIsInstance(model, self.model_class)

        model = bundle.create_model()
        self.assertIsInstance(model, self.model_class)

    def test_create_data_source(self):
        bundle = self.factory_class(self.plugin)
        ds = bundle.create_data_source()
        self.assertIsInstance(ds, self.data_source_class)
