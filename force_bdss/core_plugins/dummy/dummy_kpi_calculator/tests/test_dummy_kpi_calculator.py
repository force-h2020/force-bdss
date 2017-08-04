import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.core_plugins.dummy.dummy_kpi_calculator.dummy_kpi_calculator \
    import DummyKPICalculator
from force_bdss.core_plugins.dummy.dummy_kpi_calculator \
    .dummy_kpi_calculator_factory import DummyKPICalculatorFactory
from force_bdss.core_plugins.dummy.dummy_kpi_calculator \
    .dummy_kpi_calculator_model import DummyKPICalculatorModel


class TestDummyKPICalculator(unittest.TestCase):
    def test_run(self):
        bundle = mock.Mock(spec=DummyKPICalculatorFactory)
        kpic = DummyKPICalculator(bundle)
        model = DummyKPICalculatorModel(bundle)
        input_ = []
        output = kpic.run(model, [])
        self.assertEqual(input_, output)

    def test_slots(self):
        bundle = mock.Mock(spec=DummyKPICalculatorFactory)
        kpic = DummyKPICalculator(bundle)
        model = DummyKPICalculatorModel(bundle)
        self.assertEqual(kpic.slots(model), ((), ()))
