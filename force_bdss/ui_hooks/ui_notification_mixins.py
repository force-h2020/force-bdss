from threading import Event as ThreadingEvent

from traits.api import Instance, HasStrictTraits


class UIEventNotificationMixin(HasStrictTraits):
    #: control event that indicates whether the `STOP` signal has been
    #: received by the Listener from the UI
    _stop_event = Instance(ThreadingEvent, visible=False, transient=True)

    #: control event that indicates whether the `PAUSE` / 'RESUME' signal
    #: has been received by the Listener from the UI
    _pause_event = Instance(ThreadingEvent, visible=False, transient=True)
