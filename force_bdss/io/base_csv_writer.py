import csv

from traits.api import Unicode, Instance, List, Dict

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
    row_data = Dict(key_trait=Unicode)

    def _row_data_default(self):
        return dict.fromkeys(self.header)

    def parse_progress_event(self, event):
        """ Basic implementation of MCOProgressEvent event to row parser.
        Extracts .value attributes from `optimal_point` and `optimal_kpi`
        The MCOProgressEvent event data **MUST BE ordered** in the same way
        as the MCOStartEvent data.

        Note: this code duplicates the MCOProgressEvent handler in
        `force_wfmanager.wfmanager_setup_task._server_event_mainthread`
        Can we refactor this?
        """
        event_datavalues = event.optimal_point + event.optimal_kpis
        return [entry.value for entry in event_datavalues]

    def parse_start_event(self, event):
        """ Basic implementation of MCOStartEvent event to row parser.
        Merges the parameters' and kpis' names
        """
        return event.parameter_names + event.kpi_names

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
