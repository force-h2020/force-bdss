from traits.api import HasStrictTraits

from force_bdss.utilities import pop_dunder_recursive, nested_getstate


class BaseDriverEvent(HasStrictTraits):
    """ Base event for the MCO driver."""

    def __getstate__(self):
        """ Returns state dictionary of the object. For a nested dict,
        __getstate__ is applied to zero level items and first level items.
        """
        state = pop_dunder_recursive(super().__getstate__())
        state = nested_getstate(state)
        return state
