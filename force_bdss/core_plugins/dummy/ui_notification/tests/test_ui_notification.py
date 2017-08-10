import unittest
from testfixtures import LogCapture

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

    def test_polling(self):
        self.sync_socket.poll.return_value = 0
        listener = self.listener
        with LogCapture() as capture:
            listener.initialize(self.model)
            capture.check(
                ("force_bdss.core_plugins.dummy.ui_notification.ui_notification",  # noqa
                 "INFO",
                 "Could not connect to UI server after 1000 ms. Continuing without UI notification."  # noqa
                 ),
            )

        self.assertIsNone(listener._context)

    def test_wrong_init_recv_string(self):
        listener = self.listener

        self.sync_socket.recv_string.side_effect = [
            "HELLO\nnot_the_right_id\n1",
            "GOODBYE\nan_id\n1"
        ]

        with LogCapture() as capture:
            listener.initialize(self.model)
            capture.check(
                ("force_bdss.core_plugins.dummy.ui_notification.ui_notification",  # noqa
                 "ERROR",
                 "Unexpected reply in sync negotiation with UI server. "
                 "'HELLO\nnot_the_right_id\n1'"  # noqa
                 ),
            )

        self.assertIsNone(listener._context)

    def test_deliver_without_context(self):
        self.listener.deliver(MCOStartEvent())
        self.assertFalse(self.pub_socket.send_string.called)

    def test_finalize_without_context(self):
        self.listener.finalize()
        self.assertFalse(self.sync_socket.send_string.called)

    def test_finalize_no_response(self):
        self.sync_socket.poll.side_effect = [1, 0]
        listener = self.listener
        listener.initialize(self.model)
        with LogCapture() as capture:
            listener.finalize()
            capture.check(
                ("force_bdss.core_plugins.dummy.ui_notification.ui_notification",  # noqa
                 "INFO",
                 "Could not close connection to UI server after 1000 ms."  # noqa
                 ),
            )

        self.assertIsNone(listener._context)

    def test_wrong_finalize_recv_string(self):
        listener = self.listener
        self.sync_socket.poll.side_effect = [1, 1]
        self.sync_socket.recv_string.side_effect = [
            "HELLO\nan_id\n1",
            "GOODBYE\nnot_the_right_id\n1"
        ]

        listener.initialize(self.model)

        with LogCapture() as capture:
            listener.finalize()
            capture.check(
                ("force_bdss.core_plugins.dummy.ui_notification.ui_notification",  # noqa
                 "ERROR",
                 "Unexpected reply in goodbye sync negotiation with UI server. "  # noqa
                 "'GOODBYE\nnot_the_right_id\n1'"  # noqa
                 ),
            )

        self.assertIsNone(listener._context)
