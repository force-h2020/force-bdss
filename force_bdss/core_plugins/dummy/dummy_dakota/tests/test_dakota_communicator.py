import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin

from force_bdss.core_plugins.dummy.dummy_dakota.dakota_bundle import (
    DummyDakotaBundle)
from force_bdss.data_sources.data_source_parameters import DataSourceParameters

from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory
from force_bdss.core_plugins.dummy.dummy_dakota.parameters import \
    RangedMCOParameter


class TestDakotaCommunicator(unittest.TestCase):
    def test_receive_from_mco(self):
        bundle = DummyDakotaBundle(mock.Mock(spec=Plugin))
        mock_parameter_factory = mock.Mock(spec=BaseMCOParameterFactory)
        model = bundle.create_model()
        model.parameters = [
            RangedMCOParameter(mock_parameter_factory)
        ]
        comm = bundle.create_communicator()

        with mock.patch("sys.stdin") as stdin:
            stdin.read.return_value = "1"

            data = comm.receive_from_mco(model)
            self.assertIsInstance(data, DataSourceParameters)
            self.assertEqual(len(data.value_names), 1)
            self.assertEqual(len(data.value_types), 1)
            self.assertEqual(len(data.values), 1)
