#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

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
        """ Provides serialized form of DataSourceStartEvent
        for further data storage
        (e.g. in csv format) or processing.

        Returns:
            List(Str): input names
        """
        return self.input_names


class DataSourceFinishEvent(MCORuntimeEvent):
    """ The Data Source driver should emit this event when the
    DataSource.run method finishes."""

    #: The names assigned to the inputs.
    output_names = List(Str())

    def serialize(self):
        """ Provides serialized form of DataSourceStartEvent
        for further data storage
        (e.g. in csv format) or processing.

        Returns:
            List(Str): output names
        """
        return self.output_names
