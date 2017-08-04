import unittest
try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.kpi.base_kpi_calculator import BaseKPICalculator
from force_bdss.kpi.i_kpi_calculator_factory import IKPICalculatorFactory


class DummyKPICalculator(BaseKPICalculator):
    def run(self, *args, **kwargs):
        pass

    def slots(self, model):
        return (), ()


class TestBaseKPICalculator(unittest.TestCase):
    def test_initialization(self):
        bundle = mock.Mock(spec=IKPICalculatorFactory)
        kpic = DummyKPICalculator(bundle)

        self.assertEqual(kpic.factory, bundle)
