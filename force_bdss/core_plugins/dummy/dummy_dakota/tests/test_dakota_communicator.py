import unittest

from force_bdss.bdss_application import BDSSApplication

from force_bdss.core_plugins.dummy.dummy_dakota.dakota_bundle import (
    DummyDakotaBundle)
from force_bdss.data_sources.data_source_parameters import DataSourceParameters

from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory
from force_bdss.mco.parameters.core_mco_parameters import RangedMCOParameter

try:
    import mock
except ImportError:
    from unittest import mock


class TestDakotaCommunicator(unittest.TestCase):
    def test_receive_from_mco(self):
        bundle = DummyDakotaBundle()
        mock_application = mock.Mock(spec=BDSSApplication)
        mock_parameter_factory = mock.Mock(spec=BaseMCOParameterFactory)
        model = bundle.create_model()
        model.parameters = [
            RangedMCOParameter(mock_parameter_factory)
        ]
        comm = bundle.create_communicator(mock_application, model)

        with mock.patch("sys.stdin") as stdin:
            stdin.read.return_value = "1"

            data = comm.receive_from_mco()
            self.assertIsInstance(data, DataSourceParameters)
            self.assertEqual(len(data.value_names), 1)
            self.assertEqual(len(data.value_types), 1)
            self.assertEqual(len(data.values), 1)
