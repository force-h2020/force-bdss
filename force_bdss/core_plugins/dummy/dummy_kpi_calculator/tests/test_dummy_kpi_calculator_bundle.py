import unittest

from force_bdss.core_plugins.dummy.dummy_kpi_calculator.dummy_kpi_calculator\
    import \
    DummyKPICalculator
from force_bdss.core_plugins.dummy.dummy_kpi_calculator\
    .dummy_kpi_calculator_bundle import \
    DummyKPICalculatorBundle
from force_bdss.core_plugins.dummy.dummy_kpi_calculator\
    .dummy_kpi_calculator_model import \
    DummyKPICalculatorModel
from force_bdss.core_plugins.dummy.tests.kpi_calculator_bundle_test_mixin \
    import \
    KPICalculatorBundleTestMixin


class TestDummyKPICalculatorBundle(
        KPICalculatorBundleTestMixin, unittest.TestCase):

    @property
    def bundle_class(self):
        return DummyKPICalculatorBundle

    @property
    def kpi_calculator_class(self):
        return DummyKPICalculator

    @property
    def model_class(self):
        return DummyKPICalculatorModel
