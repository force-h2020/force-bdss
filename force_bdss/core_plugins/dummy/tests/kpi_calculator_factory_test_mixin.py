try:
    import mock
except ImportError:
    from unittest import mock

from envisage.api import Plugin


class KPICalculatorFactoryTestMixin(object):
    def setUp(self):
        self.plugin = mock.Mock(spec=Plugin)
        super(KPICalculatorFactoryTestMixin, self).setUp()

    @property
    def factory_class(self):
        raise NotImplementedError()

    @property
    def model_class(self):
        raise NotImplementedError()

    @property
    def kpi_calculator_class(self):
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

    def test_create_kpi_calculator(self):
        factory = self.factory_class(self.plugin)
        ds = factory.create_kpi_calculator()
        self.assertIsInstance(ds, self.kpi_calculator_class)
