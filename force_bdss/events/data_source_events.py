from .mco_events import MCORuntimeEvent

from traits.api import (
    List,
    Str
)


class DataSourceStartEvent(MCORuntimeEvent):
    """ The Data Source driver should emit this event when the
    DataSource.run method is called."""

    #: The names assigned to the inputs.
    input_names = List(Str())

    def serialize(self):
        """ Provides serialized form of MCOStartEvent for further data storage
        (e.g. in csv format) or processing.


        Usage example:
        For a custom MCOStartEvent subclass, this method can be overloaded.
        An example of a custom `serialize` method would be:
        >>> class CustomMCOStartEvent(DataSourceStartEvent):
        >>>
        >>>     def serialize(self):
        >>>         custom_data = [f"{name} data" for name in self.kpi_names]
        >>>         return super().serialize() + custom_data
        >>>

        Returns:
            List(Str): event parameters names and kpi names
        """
        return self.input_names


class DataSourceFinishEvent(MCORuntimeEvent):
    """ The Data Source driver should emit this event when the
    DataSource.run method finishes."""

    #: The names assigned to the inputs.
    output_names = List(Str())

    def serialize(self):
        """ Provides serialized form of MCOStartEvent for further data storage
        (e.g. in csv format) or processing.


        Usage example:
        For a custom MCOStartEvent subclass, this method can be overloaded.
        An example of a custom `serialize` method would be:
        >>> class CustomMCOStartEvent(DataSourceStartEvent):
        >>>
        >>>     def serialize(self):
        >>>         custom_data = [f"{name} data" for name in self.kpi_names]
        >>>         return super().serialize() + custom_data
        >>>

        Returns:
            List(Str): event parameters names and kpi names
        """
        return self.output_names
