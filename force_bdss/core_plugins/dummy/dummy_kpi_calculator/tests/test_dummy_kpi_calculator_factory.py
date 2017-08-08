import unittest

from force_bdss.core_plugins.dummy.dummy_kpi_calculator.dummy_kpi_calculator\
    import \
    DummyKPICalculator
from force_bdss.core_plugins.dummy.dummy_kpi_calculator\
    .dummy_kpi_calculator_factory import \
    DummyKPICalculatorFactory
from force_bdss.core_plugins.dummy.dummy_kpi_calculator\
    .dummy_kpi_calculator_model import \
    DummyKPICalculatorModel
from force_bdss.core_plugins.dummy.tests.kpi_calculator_factory_test_mixin \
    import \
    KPICalculatorFactoryTestMixin


class TestDummyKPICalculatorFactory(
        KPICalculatorFactoryTestMixin, unittest.TestCase):

    @property
    def factory_class(self):
        return DummyKPICalculatorFactory

    @property
    def kpi_calculator_class(self):
        return DummyKPICalculator

    @property
    def model_class(self):
        return DummyKPICalculatorModel
