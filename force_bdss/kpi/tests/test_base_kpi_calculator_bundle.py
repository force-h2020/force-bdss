import unittest
from envisage.plugin import Plugin

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.kpi.base_kpi_calculator_factory import \
    BaseKPICalculatorFactory


class DummyKPICalculatorBundle(BaseKPICalculatorFactory):
    id = "foo"

    name = "bar"

    def create_kpi_calculator(self):
        pass

    def create_model(self, model_data=None):
        pass


class TestBaseKPICalculatorBundle(unittest.TestCase):
    def test_initialization(self):
        bundle = DummyKPICalculatorBundle(mock.Mock(spec=Plugin))
        self.assertEqual(bundle.id, 'foo')
        self.assertEqual(bundle.name, 'bar')
