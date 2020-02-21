from .base_driver_event import BaseDriverEvent


class DataSourceStartEvent(BaseDriverEvent):
    """ The Data Source driver should emit this event when the
    DataSource.run method is called."""


class DataSourceFinishEvent(BaseDriverEvent):
    """ The Data Source driver should emit this event when the
    DataSource.run method finishes."""
