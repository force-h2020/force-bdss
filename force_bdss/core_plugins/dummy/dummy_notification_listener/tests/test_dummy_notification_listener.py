import unittest

from force_bdss.api import BaseMCOEvent
from force_bdss.notification_listeners.base_notification_listener_factory \
    import \
    BaseNotificationListenerFactory
from force_bdss.notification_listeners.base_notification_listener_model \
    import \
    BaseNotificationListenerModel
from force_bdss.tests.utils import captured_output

try:
    import mock
except ImportError:
    from unittest import mock

from force_bdss.core_plugins.dummy.dummy_notification_listener \
    .dummy_notification_listener import \
    DummyNotificationListener


class TestDummyNotificationListener(unittest.TestCase):
    def test_initialization(self):
        listener = DummyNotificationListener(
            mock.Mock(spec=BaseNotificationListenerFactory))
        model = mock.Mock(spec=BaseNotificationListenerModel)
        event = mock.Mock(spec=BaseMCOEvent)
        with captured_output() as (out, err):
            listener.initialize(model)
            listener.deliver(event)
            listener.finalize()

        self.assertEqual(out.getvalue(),
                         "Initializing\nBaseMCOEvent\nFinalizing\n")
