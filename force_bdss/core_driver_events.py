from traits.api import HasStrictTraits, Tuple, List, Instance, Float

from force_bdss.core.data_value import DataValue


class BaseDriverEvent(HasStrictTraits):
    """ Base event for the MCO driver."""


class MCOStartEvent(BaseDriverEvent):
    """ The MCO driver should emit this event when the evaluation starts."""
    input_names = Tuple()
    output_names = Tuple()


class MCOFinishEvent(BaseDriverEvent):
    """ The MCO driver should emit this event when the evaluation ends."""


class MCOProgressEvent(BaseDriverEvent):
    """ The MCO driver should emit this event for every new evaluation that has
    been completed. It carries data about the evaluation, specifically the
    input data (MCO parameter values) and the resulting output (KPIs)."""
    optimal_point = List(Instance(DataValue))
    optimal_kpis = List(Instance(DataValue))
    weights = List(Float())
