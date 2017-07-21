import unittest

from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.mco.base_multi_criteria_optimizer import \
    BaseMultiCriteriaOptimizer
from force_bdss.mco.i_multi_criteria_optimizer_bundle import \
    IMultiCriteriaOptimizerBundle

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.bdss_application import BDSSApplication


class DummyMCO(BaseMultiCriteriaOptimizer):
    def run(self, *args, **kwargs):
        pass


class TestBaseKPICalculator(unittest.TestCase):
    def test_initialization(self):
        bundle = mock.Mock(spec=IMultiCriteriaOptimizerBundle)
        application = mock.Mock(spec=BDSSApplication)
        model = mock.Mock(spec=BaseMCOModel)
        mco = DummyMCO(bundle, application, model)

        self.assertEqual(mco.bundle, bundle)
        self.assertEqual(mco.application, application)
        self.assertEqual(mco.model, model)
