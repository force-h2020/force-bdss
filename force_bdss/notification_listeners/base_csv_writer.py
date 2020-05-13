#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import csv

from traits.api import Str, Instance, List, Dict, File

from force_bdss.events.mco_events import MCOStartEvent, MCOProgressEvent
from force_bdss.notification_listeners.base_notification_listener import BaseNotificationListener # noqa
from force_bdss.notification_listeners.base_notification_listener_factory import BaseNotificationListenerFactory # noqa
from force_bdss.notification_listeners.base_notification_listener_model import BaseNotificationListenerModel # noqa


class BaseCSVWriterModel(BaseNotificationListenerModel):
    """ Base Model class for CSV writer."""

    #: CSV file path for data storage and output
    path = File("output.csv")


class BaseCSVWriter(BaseNotificationListener):
    """ Base class of core CSVWriter functionality.
    BaseCSVWriter implements basic MCOStartEvent and MCOProgressEvent
    parsers, write_to_file method, and `row_data` structure for CSV header.

    Custom implementation of the existing MCOEvent parsers should consider
    overloading only the `parse_event` adapter methods, and leave the
    `deliver` method as it is.
    """

    # A reference to the associated CSVWriterModel
    model = Instance(BaseCSVWriterModel)

    # Header to include in output CSV
    header = List(Str)

    # Data entries in CSV rows
    row_data = Dict(key_trait=Str)

    def _row_data_default(self):
        return dict.fromkeys(self.header)

    def parse_progress_event(self, event):
        """ Adapter to extract serialized data from the MCOProgressEvent event.
        The MCOProgressEvent event data **MUST BE ordered** in the same way
        as the MCOStartEvent data.
        """
        return event.serialize()

    def parse_start_event(self, event):
        """ Adapter to extract data from the MCOStartEvent event.
        """
        return event.serialize()

    def write_to_file(self, data, *, mode):
        with open(self.model.path, mode) as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def deliver(self, event):
        if isinstance(event, MCOStartEvent):
            # MCOStartEvent is considered to be an "initialization" event
            # for CSVWriter. Here the header is defined, and the row_data
            # dict is instantiated with new header keys
            self.header = self.parse_start_event(event)
            self.write_to_file(self.header, mode="w")
            self.row_data = self._row_data_default()
        elif isinstance(event, MCOProgressEvent):
            # MCOProgressEvent is considered to output the row data to
            # file, therefore the current row is finished and no additional
            # data will be accepted after this event.
            progress_data = self.parse_progress_event(event)
            for column, value in zip(self.header, progress_data):
                self.row_data[column] = value
            self.write_to_file(
                [self.row_data[el] for el in self.header], mode="a"
            )
            self.row_data = self._row_data_default()

    def initialize(self, model):
        """ Assign `model` to the writer."""
        self.model = model


class BaseCSVWriterFactory(BaseNotificationListenerFactory):
    def get_identifier(self):
        return "base_csv_writer"

    def get_name(self):
        return "Base CSV Writer"

    def get_model_class(self):
        return BaseCSVWriterModel

    def get_listener_class(self):
        return BaseCSVWriter
