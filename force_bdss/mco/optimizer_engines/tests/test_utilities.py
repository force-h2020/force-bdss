from unittest import TestCase

from force_bdss.mco.optimizer_engines.utilities import convert_by_mask


class TestConvertUtil(TestCase):
    def test_convert_by_mask(self):
        kpi_specs = ["MINIMISE", "MAXIMISE"]
        values = [10.0, 20.0]
        inv_values = convert_by_mask(values, kpi_specs)
        self.assertListEqual(list(inv_values), [10.0, -20.0])

        inv_values = convert_by_mask(values, kpi_specs, "MINIMISE")
        self.assertListEqual(list(inv_values), [10.0, -20.0])

        inv_values = convert_by_mask(values, kpi_specs, "MAXIMISE")
        self.assertListEqual(list(inv_values), [-10.0, 20.0])

        inv_values = convert_by_mask(values, kpi_specs, "SOMETHING")
        self.assertListEqual(list(inv_values), [-10.0, -20.0])
