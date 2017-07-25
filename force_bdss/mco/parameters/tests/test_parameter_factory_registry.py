import unittest

from force_bdss.mco.parameters.parameter_factory_registry import \
    ParameterFactoryRegistry


class TestParameterFactoryRegistry(unittest.TestCase):
    def test_registry_init(self):
        reg = ParameterFactoryRegistry()
        self.assertEqual(reg.factories, {})
