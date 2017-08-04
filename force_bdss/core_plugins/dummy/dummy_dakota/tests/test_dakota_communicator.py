import unittest

from force_bdss.core.data_value import DataValue

try:
    import mock
except ImportError:
    from unittest import mock

from envisage.plugin import Plugin

from force_bdss.core_plugins.dummy.dummy_dakota.dakota_factory import (
    DummyDakotaFactory)

from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory
from force_bdss.core_plugins.dummy.dummy_dakota.parameters import \
    RangedMCOParameter


class TestDakotaCommunicator(unittest.TestCase):
    def test_receive_from_mco(self):
        factory = DummyDakotaFactory(mock.Mock(spec=Plugin))
        mock_parameter_factory = mock.Mock(spec=BaseMCOParameterFactory)
        model = factory.create_model()
        model.parameters = [
            RangedMCOParameter(mock_parameter_factory)
        ]
        comm = factory.create_communicator()

        with mock.patch("sys.stdin") as stdin:
            stdin.read.return_value = "1"

            data = comm.receive_from_mco(model)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0].value, 1)
            self.assertEqual(data[0].type, "")

    def test_send_to_mco(self):
        factory = DummyDakotaFactory(mock.Mock(spec=Plugin))
        model = factory.create_model()
        comm = factory.create_communicator()

        with mock.patch("sys.stdout") as stdout:
            dv = DataValue(value=100)
            comm.send_to_mco(model, [dv, dv])
            self.assertEqual(stdout.write.call_args[0][0], '100 100')

            comm.send_to_mco(model, [])
            self.assertEqual(stdout.write.call_args[0][0], '')
