import unittest

from force_bdss.core_plugins.dummy.ui_notification.ui_notification import \
    UINotification
from force_bdss.core_plugins.dummy.ui_notification.ui_notification_factory \
    import \
    UINotificationFactory
from force_bdss.core_plugins.dummy.ui_notification.ui_notification_model \
    import \
    UINotificationModel
from force_bdss.mco.events import MCOStartEvent, MCOProgressEvent, \
    MCOFinishEvent

try:
    import mock
except ImportError:
    from unittest import mock

import zmq


class TestUINotification(unittest.TestCase):
    def setUp(self):
        factory = mock.Mock(spec=UINotificationFactory)
        self.model = UINotificationModel(factory)
        self.model.identifier = "an_id"

        listener = UINotification(factory)
        self.sync_socket = mock.Mock(spec=zmq.Socket)
        self.sync_socket.recv_string = mock.Mock()
        self.sync_socket.recv_string.side_effect = [
            "HELLO\nan_id\n1",
            "GOODBYE\nan_id\n1"
        ]

        self.pub_socket = mock.Mock(spec=zmq.Socket)
        self.context = mock.Mock(spec=zmq.Context)
        self.context.socket.side_effect = [self.pub_socket,
                                           self.sync_socket]
        listener.__class__._create_context = mock.Mock(
            return_value=self.context)

        self.listener = listener

    def test_deliver(self):
        listener = self.listener
        listener.initialize(self.model)
        self.assertEqual(
            self.sync_socket.send_string.call_args[0][0],
            'HELLO\nan_id\n1')

        listener.deliver(MCOStartEvent())
        self.assertEqual(
            self.pub_socket.send_string.call_args[0][0],
            'EVENT\nan_id\nMCO_START')

        listener.deliver(MCOProgressEvent(input=(1, 2, 3), output=(4, 5)))
        self.assertEqual(
            self.pub_socket.send_string.call_args[0][0],
            'EVENT\nan_id\nMCO_PROGRESS\n1 2 3\n4 5')

        listener.deliver(MCOFinishEvent())
        self.assertEqual(
            self.pub_socket.send_string.call_args[0][0],
            'EVENT\nan_id\nMCO_FINISH')

    def test_finalize(self):
        listener = self.listener
        listener.initialize(self.model)
        listener.finalize()
        self.assertTrue(self.context.term.called)
        self.assertTrue(self.sync_socket.close.called)
        self.assertTrue(self.pub_socket.close.called)
        self.assertIsNone(listener._context)
        self.assertIsNone(listener._sync_socket)
        self.assertIsNone(listener._pub_socket)

    def test_initialize(self):
        listener = self.listener
        listener.initialize(self.model)
        self.assertEqual(
            self.sync_socket.send_string.call_args[0][0],
            'HELLO\nan_id\n1')
