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

    def serialize(self):
        """ Provides serialized form of MCOStartEvent for further data storage
        (e.g. in csv format) or processing.

        Returns:
            List(Unicode): event parameters names and kpi names
        """
        return self.parameter_names + self.kpi_names


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

    def serialize(self):
        """ Provides serialized form of MCOProgressEvent for further data storage
        (e.g. in csv format) or processing.

        Note: this code duplicates the MCOProgressEvent handler in
        `force_wfmanager.wfmanager_setup_task._server_event_mainthread`
        Can we refactor this?

        Warning: `weights` attribute is NOT serialized here. We expect it to be
        refactored to custom MCOProgressEvent class.

        Returns:
            List(Datavalue.value): values of the event optimal points and kpis
        """
        event_datavalues = self.optimal_point + self.optimal_kpis
        return [entry.value for entry in event_datavalues]
