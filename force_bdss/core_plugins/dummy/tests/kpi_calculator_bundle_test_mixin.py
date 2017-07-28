try:
    import mock
except ImportError:
    from unittest import mock

from envisage.api import Plugin


class KPICalculatorBundleTestMixin(object):
    def setUp(self):
        self.plugin = mock.Mock(spec=Plugin)
        super(KPICalculatorBundleTestMixin, self).setUp()

    @property
    def bundle_class(self):
        raise NotImplementedError()

    @property
    def model_class(self):
        raise NotImplementedError()

    @property
    def kpi_calculator_class(self):
        raise NotImplementedError()

    def test_initialization(self):
        bundle = self.bundle_class(self.plugin)
        self.assertNotEqual(bundle.id, "")
        self.assertEqual(bundle.plugin, self.plugin)

    def test_create_model(self):
        bundle = self.bundle_class(self.plugin)
        model = bundle.create_model({})
        self.assertIsInstance(model, self.model_class)

        model = bundle.create_model()
        self.assertIsInstance(model, self.model_class)

    def test_create_kpi_calculator(self):
        bundle = self.bundle_class(self.plugin)
        ds = bundle.create_kpi_calculator()
        self.assertIsInstance(ds, self.kpi_calculator_class)
