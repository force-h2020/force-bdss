import unittest

from force_bdss.mco.base_mco_communicator import BaseMCOCommunicator
from force_bdss.mco.base_mco_model import BaseMCOModel
from force_bdss.mco.i_multi_criteria_optimizer_bundle import \
    IMultiCriteriaOptimizerBundle

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.bdss_application import BDSSApplication


class DummyMCOCommunicator(BaseMCOCommunicator):
    def receive_from_mco(self):
        pass

    def send_to_mco(self, kpi_results):
        pass


class TestBaseMCOCommunicator(unittest.TestCase):
    def test_initialization(self):
        bundle = mock.Mock(spec=IMultiCriteriaOptimizerBundle)
        application = mock.Mock(spec=BDSSApplication)
        model = mock.Mock(spec=BaseMCOModel)
        mcocomm = DummyMCOCommunicator(bundle, application, model)

        self.assertEqual(mcocomm.bundle, bundle)
        self.assertEqual(mcocomm.application, application)
        self.assertEqual(mcocomm.model, model)
