from traits.api import HasStrictTraits, Tuple


class BaseMCOEvent(HasStrictTraits):
    pass


class MCOStartEvent(BaseMCOEvent):
    pass


class MCOFinishEvent(BaseMCOEvent):
    pass


class MCOProgressEvent(BaseMCOEvent):
    input = Tuple()
    output = Tuple()
