import unittest

from force_bdss.mco.parameters.mco_parameter_factory_registry import \
    MCOParameterFactoryRegistry


class TestParameterFactoryRegistry(unittest.TestCase):
    def test_registry_init(self):
        reg = MCOParameterFactoryRegistry()
        self.assertEqual(reg.factories, {})
