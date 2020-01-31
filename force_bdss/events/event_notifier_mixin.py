from traits.api import HasStrictTraits, Event


class EventNotifierMixin(HasStrictTraits):
    """Allows the class to receive and transmit BaseDriverEvent objects"""

    #: Propagation channel for events from the Workflow objects
    event = Event()

    def notify(self, event):
        """Notify the listeners with an event. The notification will be
        synchronous. All notification listeners will receive the event, one
        after another.

        Parameters
        ----------
        event: BaseDriverEvent
            The event to broadcast.
        """
        self.event = event
