from traits.api import HasStrictTraits, List, Instance, Float, Unicode

from force_bdss.core.data_value import DataValue


class BaseDriverEvent(HasStrictTraits):
    """ Base event for the MCO driver."""


class MCOStartEvent(BaseDriverEvent):
    """ The MCO driver should emit this event when the evaluation starts."""
    #: The names assigned to the parameters.
    parameter_names = List(Unicode())

    #: The names associated to the KPIs
    kpi_names = List(Unicode())


class MCOFinishEvent(BaseDriverEvent):
    """ The MCO driver should emit this event when the evaluation ends."""


class MCOProgressEvent(BaseDriverEvent):
    """ The MCO driver should emit this event for every new optimal point
    that is found during the evaluation.
    """
    #: The point in parameter space resulting from the pareto
    #: front optimization
    optimal_point = List(Instance(DataValue))

    #: The associated KPIs to the above point
    optimal_kpis = List(Instance(DataValue))

    #: The weights assigned to the KPIs
    weights = List(Float())

    def __getstate__(self):
        d = super().__getstate__()
        d["optimal_point"] = [dv.__getstate__() for dv in d["optimal_point"]]
        d["optimal_kpis"] = [dv.__getstate__() for dv in d["optimal_kpis"]]
        return d
