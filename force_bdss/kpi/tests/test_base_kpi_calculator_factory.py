import unittest
from envisage.plugin import Plugin

from force_bdss.kpi.base_kpi_calculator import BaseKPICalculator
from force_bdss.kpi.base_kpi_calculator_model import BaseKPICalculatorModel

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.kpi.base_kpi_calculator_factory import \
    BaseKPICalculatorFactory

kpi_calculator = mock.Mock(spec=BaseKPICalculator)
kpi_calculator_model = mock.Mock(spec=BaseKPICalculatorModel)


class DummyKPICalculatorFactory(BaseKPICalculatorFactory):
    id = "foo"

    name = "bar"

    def create_kpi_calculator(self):
        pass

    def create_model(self, model_data=None):
        pass


class DummyKPICalculatorFactory2(BaseKPICalculatorFactory):
    id = "foo"

    name = "bar"

    kpi_calculator_class = kpi_calculator

    model_class = kpi_calculator_model


class TestBaseKPICalculatorFactory(unittest.TestCase):
    def test_initialization(self):
        factory = DummyKPICalculatorFactory(mock.Mock(spec=Plugin))
        self.assertEqual(factory.id, 'foo')
        self.assertEqual(factory.name, 'bar')

    def test_fast_definition(self):
        factory = DummyKPICalculatorFactory2(mock.Mock(spec=Plugin))
