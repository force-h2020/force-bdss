from traits.api import Any, List

from force_bdss.api import BaseNotificationListener
import zmq


class UINotification(BaseNotificationListener):
    _context = Any()
    _pub_socket = Any()
    _rep_socket = Any()
    _msg_cache = List()

    def deliver(self, model, message):
        try:
            data = self._rep_socket.recv(flags=zmq.NOBLOCK)
        except zmq.ZMQError:
            pass
        else:
            self._rep_socket.send_multipart(self._msg_cache)

        msg = "ACTION {}".format(message).encode("utf-8")
        self._msg_cache.append(msg)
        self._pub_socket.send(msg)

    def init_persistent_state(self, model):
        self._context = zmq.Context()
        self._pub_socket = self._context.socket(zmq.PUB)
        self._pub_socket.bind("tcp://*:12345")

        self._rep_socket = self._context.socket(zmq.REP)
        self._rep_socket.bind("tcp://*:12346")
