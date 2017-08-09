from traits.api import Any

from force_bdss.api import BaseNotificationListener
import zmq


class UINotification(BaseNotificationListener):
    _zmq_context = Any()
    _zmq_socket = Any()

    def deliver(self, model, message):
        self._zmq_socket.send(("ACTION {}".format(message)).encode("utf-8"))

    def init_persistent_state(self, model):
        self._zmq_context = zmq.Context()
        self._zmq_socket = self._zmq_context.socket(zmq.PUB)
        self._zmq_socket.bind("tcp://*:12345")
