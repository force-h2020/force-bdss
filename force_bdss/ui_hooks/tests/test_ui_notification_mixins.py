#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase
from threading import Event

from traits.api import TraitError

from force_bdss.ui_hooks.ui_notification_mixins import UIEventNotificationMixin


class TestUIEventNotificationMixin(TestCase):
    def setUp(self):
        self.ui_mixin_listener = UIEventNotificationMixin()

    def test_assignment(self):
        with self.assertRaises(TraitError):
            self.ui_mixin_listener._stop_event = 1

        event = Event()
        self.ui_mixin_listener.set_stop_event(event)
        self.ui_mixin_listener.set_pause_event(event)
        self.assertIs(self.ui_mixin_listener._stop_event, event)
        self.assertIs(self.ui_mixin_listener._pause_event, event)

    def test_send(self):
        stop_event = Event()
        pause_event = Event()
        self.ui_mixin_listener.set_stop_event(stop_event)
        self.ui_mixin_listener.set_pause_event(pause_event)
        self.assertFalse(self.ui_mixin_listener._stop_event.is_set())
        self.ui_mixin_listener.send_stop()
        self.assertTrue(self.ui_mixin_listener._stop_event.is_set())
        self.assertTrue(self.ui_mixin_listener._pause_event.is_set())

        self.ui_mixin_listener.send_pause()
        self.assertFalse(self.ui_mixin_listener._pause_event.is_set())

        self.ui_mixin_listener.send_resume()
        self.assertTrue(self.ui_mixin_listener._pause_event.is_set())
