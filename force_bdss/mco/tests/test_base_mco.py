import unittest

from force_bdss.mco.i_mco_factory import IMCOFactory
from force_bdss.tests.dummy_classes.mco import DummyMCO

try:
    import mock
except ImportError:
    from unittest import mock


class TestBaseMultiCriteriaOptimizer(unittest.TestCase):
    def test_initialization(self):
        factory = mock.Mock(spec=IMCOFactory)
        mco = DummyMCO(factory)

        self.assertEqual(mco.factory, factory)
