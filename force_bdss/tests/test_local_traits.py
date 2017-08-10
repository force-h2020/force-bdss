import unittest
from traits.api import HasStrictTraits, TraitError

from force_bdss.local_traits import Identifier, CUBAType, ZMQSocketURL


class Traited(HasStrictTraits):
    val = Identifier()
    cuba = CUBAType()
    socket_url = ZMQSocketURL()


class TestLocalTraits(unittest.TestCase):
    def test_identifier(self):
        c = Traited()

        for working in ["hello", "_hello", "_0", "_hello_123", "_", ""]:
            c.val = working
            self.assertEqual(c.val, working)

        for broken in ["0", None, 123, "0hello", "hi$", "hi%"]:
            with self.assertRaises(TraitError):
                c.val = broken

    def test_cuba_type(self):
        c = Traited()
        c.cuba = "PRESSURE"
        self.assertEqual(c.cuba, "PRESSURE")

    def test_zmq_socket_url(self):
        c = Traited()

        for working in ["tcp://127.0.0.1:12345",
                        "tcp://255.255.255.255:65535",
                        "tcp://1.1.1.1:65535"]:
            c.socket_url = working
            self.assertEqual(c.socket_url, working)

        for broken in ["tcp://270.0.0.1:12345",
                       "tcp://0.270.0.1:12345",
                       "tcp://0.0.270.1:12345",
                       "tcp://0.0.0.270:12345",
                       "url://255.255.255.255:65535",
                       "whatever",
                       "tcp://1.1.1.1:100000"]:
            with self.assertRaises(TraitError):
                c.socket_url = broken

