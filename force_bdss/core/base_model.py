from traits.api import ABCHasStrictTraits, Instance

from force_bdss.core.base_factory import BaseFactory
from force_bdss.events.event_notifier_mixin import EventNotifierMixin
from force_bdss.utilities import (
    pop_dunder_recursive,
    nested_getstate
)


class BaseModel(EventNotifierMixin, ABCHasStrictTraits):
    """Base class for all the models of all the factories."""

    #: A reference to the creating factory, so that we can
    #: retrieve it as the originating factory.
    factory = Instance(BaseFactory, visible=False, transient=True)

    def __init__(self, factory, *args, **kwargs):
        super(BaseModel, self).__init__(factory=factory, *args, **kwargs)

    def __getstate__(self):
        state = pop_dunder_recursive(super().__getstate__())
        state = nested_getstate(state)
        state = {"id": self.factory.id, "model_data": state}
        return state
