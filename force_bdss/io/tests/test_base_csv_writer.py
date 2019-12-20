from unittest import TestCase, mock

from traits.testing.unittest_tools import UnittestTools

from force_bdss.api import (
    BaseCSVWriterFactory,
    BaseCSVWriter,
    BaseCSVWriterModel,
    DataValue,
    MCOStartEvent,
    MCOProgressEvent,
)

_CSVWRITER_OPEN = "force_bdss.io.base_csv_writer.open"


class TestCSVWriter(TestCase, UnittestTools):
    def setUp(self):
        self.plugin = {"id": "id", "name": "name"}
        self.factory = BaseCSVWriterFactory(plugin=self.plugin)
        self.notification_listener = self.factory.create_listener()
        self.model = self.factory.create_model()

        self.notification_listener.initialize(self.model)

        self.parameters = [
            DataValue(name="p1", value=1.0),
            DataValue(name="p2", value=5.0),
        ]
        self.kpis = [
            DataValue(name="kpi1", value=5.7),
            DataValue(name="kpi2", value=10),
        ]

    def test_factory(self):
        self.assertEqual("base_csv_writer", self.factory.get_identifier())
        self.assertEqual("Base CSV Writer", self.factory.get_name())
        self.assertIs(self.factory.listener_class, BaseCSVWriter)
        self.assertIs(self.factory.model_class, BaseCSVWriterModel)

    def test_model(self):
        self.assertEqual("output.csv", self.model.path)

    def test_writer(self):
        self.assertEqual(self.model, self.notification_listener.model)

        new_model = self.factory.create_model()
        self.notification_listener.initialize(new_model)
        self.assertEqual(new_model, self.notification_listener.model)
        self.assertEqual({}, self.notification_listener.row_data)
        self.assertEqual([], self.notification_listener.header)

    def test_deliver_start_event(self):

        mock_open = mock.mock_open()

        with mock.patch(_CSVWRITER_OPEN, mock_open, create=True):
            event = MCOStartEvent(
                parameter_names=[p.name for p in self.parameters],
                kpi_names=[k.name for k in self.kpis],
            )
            self.assertListEqual(
                ["p1", "p2", "kpi1", "kpi2"],
                self.notification_listener.parse_start_event(event),
            )

            self.notification_listener.deliver(event)
            self.assertListEqual(
                ["p1", "p2", "kpi1", "kpi2"], self.notification_listener.header
            )
            self.assertDictEqual(
                {"p1": None, "p2": None, "kpi1": None, "kpi2": None},
                self.notification_listener.row_data,
            )

            mock_open.assert_called_once()

    def test_deliver_progress_event(self):
        mock_open = mock.mock_open()

        with mock.patch(_CSVWRITER_OPEN, mock_open, create=True):
            event = MCOProgressEvent(
                optimal_point=self.parameters, optimal_kpis=self.kpis
            )
            self.assertListEqual(
                [1.0, 5.0, 5.7, 10],
                self.notification_listener.parse_progress_event(event),
            )
            self.notification_listener.deliver(event)
            self.assertDictEqual({}, self.notification_listener.row_data)

            mock_open.assert_called_once()

        mock_open.reset_mock()

        mock_open = mock.mock_open()

        with mock.patch(_CSVWRITER_OPEN, mock_open, create=True):
            event = MCOStartEvent(
                parameter_names=[p.name for p in self.parameters],
                kpi_names=[k.name for k in self.kpis],
            )

            self.notification_listener.deliver(event)

            event = MCOProgressEvent(
                optimal_point=self.parameters, optimal_kpis=self.kpis
            )
            self.assertListEqual(
                [1.0, 5.0, 5.7, 10],
                self.notification_listener.parse_progress_event(event),
            )
            self.notification_listener.deliver(event)
            self.assertDictEqual(
                {"p1": None, "p2": None, "kpi1": None, "kpi2": None},
                self.notification_listener.row_data,
            )

        mock_open.reset_mock()
