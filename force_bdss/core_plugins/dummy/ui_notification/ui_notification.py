import errno
import logging
from traits.api import Any, List

from force_bdss.api import (
    BaseNotificationListener,
    MCOStartEvent,
    MCOFinishEvent,
    MCOProgressEvent
)

import zmq


class UINotification(BaseNotificationListener):
    """
    Notification engine for the UI. Uses zeromq for the traffic handling.
    """
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

    def initialize(self, model):
        self._context = zmq.Context()
        self._pub_socket = self._context.socket(zmq.PUB)
        self._pub_socket.bind("tcp://*:12345")

        self._rep_socket = self._context.socket(zmq.REP)
        self._rep_socket.bind("tcp://*:12346")

    def finalize(self, model):
        self._pub_socket.close()
        self._rep_socket.close()
        self._context.term()

        self._pub_socket = None
        self._rep_socket = None
        self._context = None

    def _format_event(self, event):
        if isinstance(event, MCOStartEvent):
            data = "MCO_START"
        elif isinstance(event, MCOFinishEvent):
            data = "MCO_FINISH"
        elif isinstance(event, MCOProgressEvent):
            data = "MCO_PROGRESS\n{}\n{}".format(
                " ".join([str(x) for x in event.input]),
                " ".join([str(x) for x in event.output]))
        else:
            return None

        return ("EVENT\n{}".format(data)).encode("utf-8")

