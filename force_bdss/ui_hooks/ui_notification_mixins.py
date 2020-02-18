from threading import Event as ThreadingEvent

from traits.api import Instance, HasStrictTraits


class UIEventNotificationMixin(HasStrictTraits):
    """ The UIEventNotificationMixin contains the _stop and _pause
    threading.Event instances, and implements basic API to send the
    stop or pause / resume commands via these events."""

    #: control event that indicates whether the `STOP` signal has been
    #: received by the Listener from the UI
    _stop_event = Instance(ThreadingEvent, visible=False, transient=True)

    #: control event that indicates whether the `PAUSE` / 'RESUME' signal
    #: has been received by the Listener from the UI
    _pause_event = Instance(ThreadingEvent, visible=False, transient=True)

    def set_stop_event(self, event):
        self._stop_event = event

    def set_pause_event(self, event):
        self._pause_event = event

    def send_stop(self):
        self._pause_event.set()
        self._stop_event.set()

    def send_pause(self):
        self._pause_event.clear()

    def send_resume(self):
        self._pause_event.set()
