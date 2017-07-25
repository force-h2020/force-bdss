import unittest

from force_bdss.mco.parameters import core_mco_parameters
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory


class TestCoreMCOParameters(unittest.TestCase):
    def test_all_classes(self):
        factories = core_mco_parameters.all_core_factories()
        self.assertNotEqual(len(factories), 0)

        for f in factories:
            self.assertTrue(issubclass(f, BaseMCOParameterFactory))
