import errno
import logging
from traits.api import Any, List

from force_bdss.api import BaseNotificationListener
import zmq


class UINotification(BaseNotificationListener):
    #: The ZMQ context.
    _context = Any()

    #: The pubsub socket.
    _pub_socket = Any()

    #: The synchronization socket to recover already sent information at a
    #: later stage
    _rep_socket = Any()

    #: The cache of messages as they are sent out.
    _msg_cache = List()

    def deliver(self, model, message):
        try:
            data = self._rep_socket.recv(flags=zmq.NOBLOCK)
        except zmq.ZMQError as e:
            if e.errno == errno.EAGAIN:
                data = None
            else:
                logging.error("Error while receiving data from "
                              "reply socket: {}".format(str(e)))

        if data and data[0:4] == "SYNC".encode("utf-8"):
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
