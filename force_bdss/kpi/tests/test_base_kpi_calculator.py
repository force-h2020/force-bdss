import unittest
try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.bdss_application import BDSSApplication
from force_bdss.kpi.base_kpi_calculator_model import BaseKPICalculatorModel
from force_bdss.kpi.base_kpi_calculator import BaseKPICalculator
from force_bdss.kpi.i_kpi_calculator_bundle import IKPICalculatorBundle


class DummyKPICalculator(BaseKPICalculator):
    def run(self, *args, **kwargs):
        pass


class TestBaseKPICalculator(unittest.TestCase):
    def test_initialization(self):
        bundle = mock.Mock(spec=IKPICalculatorBundle)
        application = mock.Mock(spec=BDSSApplication)
        model = mock.Mock(spec=BaseKPICalculatorModel)
        kpic = DummyKPICalculator(bundle, application, model)

        self.assertEqual(kpic.bundle, bundle)
        self.assertEqual(kpic.application, application)
        self.assertEqual(kpic.model, model)
