import csv

from traits.api import Unicode, Instance, List

from force_bdss.api import (
    BaseNotificationListenerFactory,
    BaseNotificationListenerModel,
    BaseNotificationListener,
    MCOProgressEvent,
    MCOStartEvent,
)


class BaseCSVWriterModel(BaseNotificationListenerModel):
    path = Unicode("output.csv")


class BaseCSVWriter(BaseNotificationListener):

    # A reference to the associated CSVWriterModel
    model = Instance(BaseCSVWriterModel)

    # Header to include in output CSV
    header = List(Unicode)

    # Data entries in CSV rows
    row_data = List

    def _row_data_default(self):
        return []

    def parse_progress_event(self, event):
        """ Basic implementation of event to row parser.

        Note: this code duplicates the MCOProgressEvent handler in
        `force_wfmanager.wfmanager_setup_task._server_event_mainthread`
        Can we refactor this?
        """
        row = [dv.value for dv in event.optimal_point]
        row.extend([dv.value for dv in event.optimal_kpis])
        return row

    def parse_start_event(self, event):
        header = list(event.parameter_names)
        header.extend(list(event.kpi_names))
        return header

    def write_to_file(self, data, *, mode):
        with open(self.model.path, mode) as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def deliver(self, event):
        if isinstance(event, MCOStartEvent):
            self.header = self.parse_start_event(event)
            self.write_to_file(self.header, mode="w")
        elif isinstance(event, MCOProgressEvent):
            self.row_data = self.parse_progress_event(event)
            self.write_to_file(self.row_data, mode="a")
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
