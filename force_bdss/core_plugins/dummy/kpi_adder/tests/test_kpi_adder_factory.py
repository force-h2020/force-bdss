import unittest

from force_bdss.core_plugins.dummy.kpi_adder.kpi_adder_factory import \
    KPIAdderFactory
from force_bdss.core_plugins.dummy.kpi_adder.kpi_adder_calculator import \
    KPIAdderCalculator
from force_bdss.core_plugins.dummy.kpi_adder.kpi_adder_model import \
    KPIAdderModel
from force_bdss.core_plugins.dummy.tests.kpi_calculator_factory_test_mixin \
    import \
    KPICalculatorFactoryTestMixin


class TestDummyKPICalculatorFactory(
        KPICalculatorFactoryTestMixin, unittest.TestCase):

    @property
    def factory_class(self):
        return KPIAdderFactory

    @property
    def kpi_calculator_class(self):
        return KPIAdderCalculator

    @property
    def model_class(self):
        return KPIAdderModel
