from traits.api import HasStrictTraits, Tuple, Str


class BaseDriverEvent(HasStrictTraits):
    """Base event for the Driver"""


class MCOStartEvent(BaseDriverEvent):
    """MCO should emit this event when the evaluation starts."""
    input_names = Str()
    output_names = Str()


class MCOFinishEvent(BaseDriverEvent):
    """MCO should emit this event when the evaluation ends."""


class MCOProgressEvent(BaseDriverEvent):
    """MCO should emit this event for every new evaluation that has been
    completed. It carries data about the evaluation, specifically the
    input data (MCO parameter values) and the resulting output (KPIs)."""
    input = Tuple()
    output = Tuple()
