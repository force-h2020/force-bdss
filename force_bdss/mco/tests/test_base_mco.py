import unittest

from force_bdss.mco.base_mco import BaseMCO
from force_bdss.mco.i_mco_factory import IMCOFactory

try:
    import mock
except ImportError:
    from unittest import mock


class DummyMCO(BaseMCO):
    def run(self, model, *args, **kwargs):
        pass


class TestBaseMultiCriteriaOptimizer(unittest.TestCase):
    def test_initialization(self):
        bundle = mock.Mock(spec=IMCOFactory)
        mco = DummyMCO(bundle)

        self.assertEqual(mco.factory, bundle)
