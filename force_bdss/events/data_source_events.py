from .mco_events import MCORuntimeEvent


class DataSourceStartEvent(MCORuntimeEvent):
    """ The Data Source driver should emit this event when the
    DataSource.run method is called."""


class DataSourceFinishEvent(MCORuntimeEvent):
    """ The Data Source driver should emit this event when the
    DataSource.run method finishes."""
