from traits.api import HasStrictTraits, Tuple


class BaseMCOEvent(HasStrictTraits):
    """Base event for the MCO"""


class MCOStartEvent(BaseMCOEvent):
    """MCO should emit this event when the evaluation starts."""


class MCOFinishEvent(BaseMCOEvent):
    """MCO should emit this event when the evaluation ends."""


class MCOProgressEvent(BaseMCOEvent):
    """MCO should emit this event for every new evaluation that has been
    completed. It carries data about the evaluation, specifically the
    input data (MCO parameter values) and the resulting output (KPIs)."""
    input = Tuple()
    output = Tuple()
