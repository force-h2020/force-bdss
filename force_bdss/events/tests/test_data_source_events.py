#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase

from force_bdss.events.data_source_events import (
    DataSourceStartEvent,
    DataSourceFinishEvent,
)
from force_bdss.events.mco_events import MCORuntimeEvent


class TestDataSourceEvents(TestCase):
    def test_getstate_start_event(self):
        event = DataSourceStartEvent()
        self.assertDictEqual(
            event.__getstate__(),
            {
                "model_data": {"input_names": []},
                "id": "force_bdss.events.data_source_events."
                "DataSourceStartEvent",
            },
        )
        self.assertIsInstance(event, MCORuntimeEvent)

    def test_getstate_finish_event(self):
        event = DataSourceFinishEvent()
        self.assertDictEqual(
            event.__getstate__(),
            {
                "model_data": {"output_names": []},
                "id": "force_bdss.events.data_source_events."
                "DataSourceFinishEvent",
            },
        )
        self.assertIsInstance(event, MCORuntimeEvent)

    def test_serialize_finish_event(self):
        event = DataSourceFinishEvent()

        self.assertListEqual(event.serialize(), [])

    def test_serialize_start_event(self):
        event = DataSourceStartEvent()

        self.assertListEqual(event.serialize(), [])
