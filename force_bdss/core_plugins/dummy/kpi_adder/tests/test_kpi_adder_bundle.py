import unittest

from force_bdss.core_plugins.dummy.kpi_adder.kpi_adder_bundle import \
    KPIAdderBundle
from force_bdss.core_plugins.dummy.kpi_adder.kpi_adder_calculator import \
    KPIAdderCalculator
from force_bdss.core_plugins.dummy.kpi_adder.kpi_adder_model import \
    KPIAdderModel
from force_bdss.core_plugins.dummy.tests.kpi_calculator_bundle_test_mixin \
    import \
    KPICalculatorBundleTestMixin


class TestDummyKPICalculatorBundle(
        KPICalculatorBundleTestMixin, unittest.TestCase):

    @property
    def bundle_class(self):
        return KPIAdderBundle

    @property
    def kpi_calculator_class(self):
        return KPIAdderCalculator

    @property
    def model_class(self):
        return KPIAdderModel
