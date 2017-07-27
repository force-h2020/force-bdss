import unittest
try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.kpi.base_kpi_calculator import BaseKPICalculator
from force_bdss.kpi.i_kpi_calculator_bundle import IKPICalculatorBundle


class DummyKPICalculator(BaseKPICalculator):
    def run(self, *args, **kwargs):
        pass


class TestBaseKPICalculator(unittest.TestCase):
    def test_initialization(self):
        bundle = mock.Mock(spec=IKPICalculatorBundle)
        kpic = DummyKPICalculator(bundle)

        self.assertEqual(kpic.bundle, bundle)
