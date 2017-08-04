import unittest

from force_bdss.mco.base_mco_communicator import BaseMCOCommunicator
from force_bdss.mco.i_mco_factory import IMCOFactory

try:
    import mock
except ImportError:
    from unittest import mock


class DummyMCOCommunicator(BaseMCOCommunicator):
    def receive_from_mco(self, model):
        pass

    def send_to_mco(self, model, kpi_results):
        pass


class TestBaseMCOCommunicator(unittest.TestCase):
    def test_initialization(self):
        bundle = mock.Mock(spec=IMCOFactory)
        mcocomm = DummyMCOCommunicator(bundle)

        self.assertEqual(mcocomm.bundle, bundle)
