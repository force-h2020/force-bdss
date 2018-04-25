import unittest
import testfixtures
from envisage.plugin import Plugin

from force_bdss.kpi.tests.test_base_kpi_calculator import DummyKPICalculator
from force_bdss.kpi.tests.test_base_kpi_calculator_model import \
    DummyKPICalculatorModel

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.kpi.base_kpi_calculator_factory import \
    BaseKPICalculatorFactory


class DummyKPICalculatorFactory(BaseKPICalculatorFactory):
    id = "foo"

    name = "bar"

    def create_kpi_calculator(self):
        pass

    def create_model(self, model_data=None):
        pass


class DummyKPICalculatorFactoryFast(BaseKPICalculatorFactory):
    id = "foo"

    name = "bar"

    kpi_calculator_class = DummyKPICalculator

    model_class = DummyKPICalculatorModel


class TestBaseKPICalculatorFactory(unittest.TestCase):
    def test_initialization(self):
        factory = DummyKPICalculatorFactory(mock.Mock(spec=Plugin))
        self.assertEqual(factory.id, 'foo')
        self.assertEqual(factory.name, 'bar')

    def test_fast_definition(self):
        factory = DummyKPICalculatorFactoryFast(mock.Mock(spec=Plugin))
        self.assertIsInstance(factory.create_kpi_calculator(),
                              DummyKPICalculator)

        self.assertIsInstance(factory.create_model(),
                              DummyKPICalculatorModel)

    def test_fast_definition_errors(self):
        factory = DummyKPICalculatorFactoryFast(mock.Mock(spec=Plugin))
        factory.kpi_calculator_class = None
        factory.model_class = None

        with testfixtures.LogCapture():
            with self.assertRaises(RuntimeError):
                factory.create_kpi_calculator()

            with self.assertRaises(RuntimeError):
                factory.create_model()
