import unittest

from force_bdss.core_plugins.dummy.ui_notification.ui_notification import \
    UINotification
from force_bdss.core_plugins.dummy.ui_notification.ui_notification_factory \
    import \
    UINotificationFactory
from force_bdss.core_plugins.dummy.ui_notification.ui_notification_model \
    import \
    UINotificationModel
from force_bdss.mco.events import MCOStartEvent

try:
    import mock
except ImportError:
    from unittest import mock

import zmq


class TestUINotification(unittest.TestCase):
    def setUp(self):
        self.context = mock.Mock(spec=zmq.Context)
        self.rep_socket = mock.Mock(spec=zmq.Socket)
        self.pub_socket = mock.Mock(spec=zmq.Socket)

        listener = UINotification(
            mock.Mock(spec=UINotificationFactory)
        )
        listener._context = self.context
        listener._rep_socket = self.rep_socket
        listener._pub_socket = self.pub_socket
        listener._rep_socket.recv.return_value = "SYNC".encode("utf-8")
        self.listener = listener

    def test_deliver(self):
        listener = self.listener
        listener.deliver(mock.Mock(spec=UINotificationModel), MCOStartEvent())
        self.assertEqual(
            listener._rep_socket.send_multipart.call_args[0][0],
            ['EVENT\nMCO_START'.encode('utf-8')])
        self.assertEqual(
            listener._pub_socket.send.call_args[0][0],
            'EVENT\nMCO_START'.encode('utf-8'))

    def test_finalize(self):
        listener = self.listener
        listener.finalize(mock.Mock())
        self.assertTrue(self.context.term.called)
        self.assertTrue(self.rep_socket.close.called)
        self.assertTrue(self.pub_socket.close.called)
        self.assertIsNone(listener._context)
        self.assertIsNone(listener._rep_socket)
        self.assertIsNone(listener._pub_socket)

    def test_initialize(self):
        with mock.patch('force_bdss.core_plugins.dummy.ui_notification.'
                        'ui_notification.zmq') as mock_zmq:
            mock_zmq.Context.return_value = self.context
            self.context.socket.return_value = self.rep_socket
            listener = UINotification(
                mock.Mock(spec=UINotificationFactory)
            )
            listener.initialize(mock.Mock())
            self.assertTrue(listener._pub_socket.bind.called)
