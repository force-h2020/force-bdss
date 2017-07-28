import unittest

from force_bdss.core_plugins.dummy.dummy_dakota import parameters
from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory


class TestCoreMCOParameters(unittest.TestCase):
    def test_all_factories(self):
        factories = parameters.all_core_factories()
        self.assertEqual(len(factories), 1)

        for f in factories:
            self.assertIsInstance(f, BaseMCOParameterFactory)
