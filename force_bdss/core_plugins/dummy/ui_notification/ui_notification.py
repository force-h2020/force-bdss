import errno
import logging
from traits.api import Any, List, Instance

from force_bdss.api import BaseNotificationListener
import zmq

from force_bdss.mco.events import BaseMCOEvent, MCOStartEvent, MCOFinishEvent, \
    MCOProgressEvent


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

    def deliver(self, model, event):
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

        msg = self._format_event(event)
        if msg is not None:
            self._msg_cache.append(msg)
            self._pub_socket.send(msg)

    def init_persistent_state(self, model):
        self._context = zmq.Context()
        self._pub_socket = self._context.socket(zmq.PUB)
        self._pub_socket.bind("tcp://*:12345")

        self._rep_socket = self._context.socket(zmq.REP)
        self._rep_socket.bind("tcp://*:12346")

    def _format_event(self, event):
        if isinstance(event, MCOStartEvent):
            data = "MCO_START"
        elif isinstance(event, MCOFinishEvent):
            data = "MCO_FINISH"
        elif isinstance(event, MCOProgressEvent):
            data = "MCO_PROGRESS {} {}".format(event.input, event.output)
        else:
            return None

        return ("EVENT {}".format(data)).encode("utf-8")
