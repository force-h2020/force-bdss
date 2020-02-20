from json import dumps
import unittest

from force_bdss.core.data_value import DataValue
from force_bdss.events.base_driver_event import BaseDriverEvent
from force_bdss.events.mco_events import (
    MCOProgressEvent,
    WeightedMCOProgressEvent,
    MCOStartEvent,
    WeightedMCOStartEvent,
    MCOFinishEvent,
    MCOTerminateEvent
)


class TestMCOEvents(unittest.TestCase):

    def test_getstate_progress_event(self):
        ev = MCOProgressEvent(
            optimal_kpis=[DataValue(value=10)],
            optimal_point=[DataValue(value=12), DataValue(value=13)],
        )

        self.assertEqual(
            ev.__getstate__(),
            {
                "id": "force_bdss.events.mco_events.MCOProgressEvent",
                "model_data": {
                    "optimal_kpis": [
                        {
                            "accuracy": None,
                            "name": "",
                            "quality": "AVERAGE",
                            "type": "",
                            "value": 10,
                        }
                    ],
                    "optimal_point": [
                        {
                            "accuracy": None,
                            "name": "",
                            "quality": "AVERAGE",
                            "type": "",
                            "value": 12,
                        },
                        {
                            "accuracy": None,
                            "name": "",
                            "quality": "AVERAGE",
                            "type": "",
                            "value": 13,
                        },
                    ],
                },
            },
        )

    def test_getstate_start_event(self):
        event = MCOStartEvent(
            parameter_names=["p1", "p2"], kpi_names=["k1", "k2", "k3"]
        )
        self.assertDictEqual(
            event.__getstate__(),
            {
                "model_data": {
                    "parameter_names": ["p1", "p2"],
                    "kpi_names": ["k1", "k2", "k3"],
                },
                "id": "force_bdss.events.mco_events.MCOStartEvent",
            },
        )

    def test_getstate_finish_event(self):
        event = MCOFinishEvent()
        self.assertDictEqual(
            event.__getstate__(),
            {
                "model_data": {},
                "id": "force_bdss.events.mco_events.MCOFinishEvent",
            },
        )

    def test_getstate_terminate_event(self):
        event = MCOTerminateEvent()
        self.assertDictEqual(
            event.__getstate__(),
            {
                "model_data": {},
                "id": "force_bdss.events.mco_events.MCOTerminateEvent",
            },
        )

    def test_serialize_start_event(self):
        event = MCOStartEvent(
            parameter_names=["p1", "p2"], kpi_names=["k1", "k2", "k3"]
        )
        self.assertListEqual(["p1", "p2", "k1", "k2", "k3"], event.serialize())

        event = WeightedMCOStartEvent(
            parameter_names=["p1", "p2"], kpi_names=["k1", "k2", "k3"]
        )
        self.assertListEqual(
            [
                "p1",
                "p2",
                "k1",
                "k1 weight",
                "k2",
                "k2 weight",
                "k3",
                "k3 weight",
            ],
            event.serialize(),
        )

    def test_serialize_progress_event(self):
        event = MCOProgressEvent(
            optimal_kpis=[DataValue(value=10)],
            optimal_point=[DataValue(value=12), DataValue(value=13)],
        )

        self.assertListEqual(event.serialize(), [12, 13, 10])

        event = WeightedMCOProgressEvent(
            optimal_kpis=[DataValue(value=10)],
            optimal_point=[DataValue(value=12), DataValue(value=13)],
            weights=[1.0],
        )

        self.assertListEqual([12, 13, 10, 1.0], event.serialize())

    def test_default_weights_weighted_progress_event(self):
        event = WeightedMCOProgressEvent(
            optimal_kpis=[DataValue(value=10)],
            optimal_point=[DataValue(value=12), DataValue(value=13)],
        )
        self.assertEqual(len(event.optimal_kpis), len(event.weights))
        self.assertListEqual(
            event.weights,
            [1.0 / len(event.optimal_kpis)] * len(event.optimal_kpis),
        )
        self.assertEqual(event.serialize(), [12, 13, 10, 1.0])

        event = WeightedMCOProgressEvent(
            optimal_kpis=[],
            optimal_point=[DataValue(value=12), DataValue(value=13)],
        )
        self.assertEqual(len(event.optimal_kpis), len(event.weights))
        self.assertListEqual(event.weights, [])
        self.assertEqual(event.serialize(), [12, 13])

    def test_get_event_class(self):

        data = {
            "id": "force_bdss.events.mco_events.MCOProgressEvent",
            "model_data": {},
        }
        klass = MCOProgressEvent.get_event_class(data["id"])
        self.assertIs(klass, MCOProgressEvent)

        data = {
            "id": "force_bdss.events.mco_events.MCOStartEvent",
            "model_data": {},
        }
        klass = BaseDriverEvent.get_event_class(data["id"])
        self.assertIs(klass, MCOStartEvent)

        data = {
            "id": "force_bdss.events.mco_events.MCOFinishEvent",
            "model_data": {},
        }
        klass = BaseDriverEvent.get_event_class(data["id"])
        self.assertIs(klass, MCOFinishEvent)

    def test_from_json(self):

        start_data = {
            "model_data": {
                "parameter_names": ["p1", "p2"],
                "kpi_names": ["k1", "k2", "k3"],
            },
            "id": "force_bdss.events.mco_events.MCOStartEvent",
        }
        start_event = BaseDriverEvent.from_json(start_data)
        self.assertIsInstance(start_event, MCOStartEvent)
        self.assertDictEqual(start_event.__getstate__(), start_data)

        finish_data = {
            "id": "force_bdss.events.mco_events.MCOFinishEvent",
            "model_data": {},
        }
        finish_event = BaseDriverEvent.from_json(finish_data)
        self.assertIsInstance(finish_event, MCOFinishEvent)
        self.assertDictEqual(finish_event.__getstate__(), finish_data)

        progress_data = {
            "id": "force_bdss.events.mco_events.MCOProgressEvent",
            "model_data": {
                "optimal_kpis": [
                    {
                        "accuracy": None,
                        "name": "",
                        "quality": "AVERAGE",
                        "type": "",
                        "value": 10,
                    }
                ],
                "optimal_point": [
                    {
                        "accuracy": None,
                        "name": "",
                        "quality": "AVERAGE",
                        "type": "",
                        "value": 12,
                    },
                    {
                        "accuracy": None,
                        "name": "",
                        "quality": "AVERAGE",
                        "type": "",
                        "value": 13,
                    },
                ],
            },
        }
        progress_event = BaseDriverEvent.from_json(progress_data)
        self.assertIsInstance(progress_event, MCOProgressEvent)
        self.assertDictEqual(progress_event.__getstate__(), progress_data)

    def test_raises_from_json(self):
        failed_data = {
            "id": "force_bdss.events.mco_events.MCOProgressEvent",
            "model_data": {
                "optimal_kpis": [{"random_trait": "some data"}],
                "optimal_point": [],
            },
        }
        with self.assertRaisesRegex(
            Exception,
            r"Unable to instantiate a \<class "
            r"'force_bdss.events.mco_events.MCOProgressEvent'\> "
            r"instance with data "
            r"\{'optimal_kpis': \[\{'random_trait': 'some data'\}\],"
            r" 'optimal_point': \[\]}"
            r": the `__init__` and `from_json` "
            r"methods failed to create an instance.",
        ):
            BaseDriverEvent.from_json(failed_data)

    def test_loads_json(self):
        start_data = {
            "model_data": {
                "parameter_names": ["p1", "p2"],
                "kpi_names": ["k1", "k2", "k3"],
            },
            "id": "force_bdss.events.mco_events.MCOStartEvent",
        }
        start_event = BaseDriverEvent.loads_json(dumps(start_data))
        self.assertIsInstance(start_event, MCOStartEvent)
        self.assertDictEqual(start_event.__getstate__(), start_data)
        self.assertEqual(start_event.dumps_json(), dumps(start_data))

    def test_dumps_json(self):
        start_data = {
            "model_data": {
                "parameter_names": ["p1", "p2"],
                "kpi_names": ["k1", "k2", "k3"],
            },
            "id": "force_bdss.events.mco_events.MCOStartEvent",
        }
        start_event = BaseDriverEvent.from_json(start_data)
        json_dump = start_event.dumps_json()
        self.assertIn('"parameter_names": ["p1", "p2"]', json_dump)
        self.assertIn('"kpi_names": ["k1", "k2", "k3"]', json_dump)
        self.assertIn('"parameter_names": ["p1", "p2"]', json_dump)
        self.assertIn('"model_data": {', json_dump)
        self.assertIn(
            '"id": "force_bdss.events.mco_events.MCOStartEvent"', json_dump
        )
        self.assertEqual(len(str(start_data)), len(json_dump))
