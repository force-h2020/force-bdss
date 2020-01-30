from traits.api import ABCHasStrictTraits, Instance, Event

from force_bdss.core.base_factory import BaseFactory
from force_bdss.utilities import (
    pop_dunder_recursive,
    nested_getstate
)


class BaseModel(ABCHasStrictTraits):
    """Base class for all the models of all the factories."""

    #: A reference to the creating factory, so that we can
    #: retrieve it as the originating factory.
    factory = Instance(BaseFactory, visible=False, transient=True)

    #: Propagation channel for events from the Workflow objects
    event = Event()

    def __init__(self, factory, *args, **kwargs):
        super(BaseModel, self).__init__(factory=factory, *args, **kwargs)

    def __getstate__(self):
        state = pop_dunder_recursive(super().__getstate__())
        state = nested_getstate(state)
        state = {"id": self.factory.id, "model_data": state}
        return state

    def notify(self, event):
        """Notify the listeners with an event. The notification will be
        synchronous. All notification listeners will receive the event, one
        after another.

        Parameters
        ----------
        event: BaseMCOEvent
            The event to broadcast.
        """
        self.event = event
