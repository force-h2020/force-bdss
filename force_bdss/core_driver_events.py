from traits.api import HasStrictTraits, List, Instance, Float, Unicode

from force_bdss.core.data_value import DataValue
from force_bdss.io.workflow_writer import pop_dunder_recursive


class BaseDriverEvent(HasStrictTraits):
    """ Base event for the MCO driver."""

    def __getstate__(self):
        state = pop_dunder_recursive(super().__getstate__())
        for key in state:
            # We safely attempt to get state of the zero and first
            # level objects of the object state dictionary
            try:
                if isinstance(state[key], (tuple, list)):
                    state[key] = [el.__getstate__() for el in state[key]]
                else:
                    state[key] = state[key].__getstate__()
            except AttributeError:
                pass

        return state


class MCOStartEvent(BaseDriverEvent):
    """ The MCO driver should emit this event when the evaluation starts."""

    #: The names assigned to the parameters.
    parameter_names = List(Unicode())

    #: The names associated to the KPIs
    kpi_names = List(Unicode())


class MCOFinishEvent(BaseDriverEvent):
    """ The MCO driver should emit this event when the evaluation ends."""


class MCOProgressEvent(BaseDriverEvent):
    """ The MCO driver should emit this event for every new point that is
    evaluated during the MCO run.
    """

    #: The point in parameter space resulting from the pareto
    #: front optimization
    optimal_point = List(Instance(DataValue))

    #: The associated KPIs to the above point
    optimal_kpis = List(Instance(DataValue))

    #: The weights assigned to the KPIs
    weights = List(Float())
