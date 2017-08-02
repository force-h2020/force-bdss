import unittest

from force_bdss.core.data_value import DataValue
from force_bdss.core_plugins.dummy.kpi_adder.kpi_adder_model import \
    KPIAdderModel
from force_bdss.kpi.base_kpi_calculator_bundle import BaseKPICalculatorBundle

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.core_plugins.dummy.kpi_adder.kpi_adder_calculator import \
    KPIAdderCalculator


class TestKPIAdderCalculator(unittest.TestCase):
    def test_basic_functionality(self):
        kpic = KPIAdderCalculator(mock.Mock(spec=BaseKPICalculatorBundle))
        model = KPIAdderModel(mock.Mock(spec=BaseKPICalculatorBundle))
        model.cuba_type_in = "PRESSURE"
        model.cuba_type_out = "TOTAL_PRESSURE"
        dv1 = DataValue(type="PRESSURE", value=10)
        dv2 = DataValue(type="PRESSURE", value=30)
        dv3 = DataValue(type="VOLUME", value=100)
        res = kpic.run(model, [dv1, dv2, dv3])
        self.assertEqual(res[0].type, "TOTAL_PRESSURE")
        self.assertEqual(res[0].value, 40)

    def test_slots(self):
        kpic = KPIAdderCalculator(mock.Mock(spec=BaseKPICalculatorBundle))
        model = KPIAdderModel(mock.Mock(spec=BaseKPICalculatorBundle))
        in_slot, out_slot = kpic.slots(model)
        self.assertEqual(len(in_slot), 3)
        self.assertEqual(len(out_slot), 1)

