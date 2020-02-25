from unittest import TestCase

from force_bdss.events.data_source_events import (
    DataSourceStartEvent,
    DataSourceFinishEvent,
)
from force_bdss.events.mco_events import MCORuntimeEvent


class TestDataSourceEvents(TestCase):
    def test_getstate_start_event(self):
        event = DataSourceStartEvent(name="name")
        self.assertDictEqual(
            event.__getstate__(),
            {
                "model_data": {"name": "name"},
                "id": "force_bdss.events.data_source_events."
                "DataSourceStartEvent",
            },
        )
        self.assertIsInstance(event, MCORuntimeEvent)

    def test_getstate_finish_event(self):
        event = DataSourceFinishEvent(name="name")
        self.assertDictEqual(
            event.__getstate__(),
            {
                "model_data": {"name": "name"},
                "id": "force_bdss.events.data_source_events."
                "DataSourceFinishEvent",
            },
        )
        self.assertIsInstance(event, MCORuntimeEvent)
