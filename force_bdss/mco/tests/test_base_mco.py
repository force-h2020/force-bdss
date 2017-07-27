import unittest

from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.mco.base_mco import BaseMCO
from force_bdss.mco.i_mco_bundle import IMCOBundle

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.bdss_application import BDSSApplication


class DummyMCO(BaseMCO):
    def run(self, *args, **kwargs):
        pass


class TestBaseMultiCriteriaOptimizer(unittest.TestCase):
    def test_initialization(self):
        bundle = mock.Mock(spec=IMCOBundle)
        application = mock.Mock(spec=BDSSApplication)
        model = mock.Mock(spec=BaseMCOModel)
        mco = DummyMCO(bundle, application, model)

        self.assertEqual(mco.bundle, bundle)
        self.assertEqual(mco.application, application)
        self.assertEqual(mco.model, model)
