import unittest

from force_bdss.kpi.base_kpi_calculator_bundle import \
    BaseKPICalculatorBundle


class DummyKPICalculatorBundle(BaseKPICalculatorBundle):
    id = "foo"

    name = "bar"

    def create_kpi_calculator(self, application, model):
        pass

    def create_model(self, model_data=None):
        pass


class TestBaseKPICalculatorBundle(unittest.TestCase):
    def test_initialization(self):
        bundle = DummyKPICalculatorBundle()
        self.assertEqual(bundle.id, 'foo')
        self.assertEqual(bundle.name, 'bar')
