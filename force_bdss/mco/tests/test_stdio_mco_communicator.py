from io import StringIO
from unittest import TestCase, mock

from force_bdss.api import DataValue
from force_bdss.mco.i_mco_factory import IMCOFactory
from force_bdss.mco.stdio_mco_communicator import StdIOMCOCommunicator


class DummyModel:
    pass


class DummyParameter:
    pass


class TestStdIOMCOCommunicator(TestCase):
    def setUp(self):
        self.factory = mock.Mock(spec=IMCOFactory)
        self.communicator = StdIOMCOCommunicator(self.factory)

    def test_initialize(self):
        self.assertIs(self.communicator.factory, self.factory)

    def test_receive_from_mco(self):
        model = DummyModel()
        parameters = [DummyParameter(), DummyParameter(), DummyParameter()]
        for parameter in parameters:
            parameter.name = "name"
            parameter.type = "type"
        model.parameters = parameters

        values = "1 2 3"
        with mock.patch("sys.stdin.read", return_value=values):
            output = self.communicator.receive_from_mco(model)
        self.assertEqual(3, len(output))
        for i, data in enumerate(output):
            self.assertIsInstance(data, DataValue)
            self.assertEqual("name", data.name)
            self.assertEqual("type", data.type)
            self.assertEqual(i + 1, data.value)

    def test_send_to_mco(self):
        parameters = [DummyParameter(), DummyParameter(), DummyParameter()]
        for i, parameter in enumerate(parameters):
            parameter.value = i

        with mock.patch("sys.stdout", new=StringIO()) as patched_stdout:
            self.communicator.send_to_mco(None, parameters)
            self.assertEqual(patched_stdout.getvalue().strip(), "0 1 2")
