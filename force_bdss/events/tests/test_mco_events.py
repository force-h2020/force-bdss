import unittest

from force_bdss.core.data_value import DataValue
from force_bdss.events.mco_events import (
    MCOProgressEvent,
    WeightedMCOProgressEvent,
    MCOStartEvent,
    WeightedMCOStartEvent,
    MCOFinishEvent,
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
        )

    def test_getstate_start_event(self):
        event = MCOStartEvent(
            parameter_names=["p1", "p2"], kpi_names=["k1", "k2", "k3"]
        )
        self.assertDictEqual(
            event.__getstate__(),
            {"parameter_names": ["p1", "p2"], "kpi_names": ["k1", "k2", "k3"]},
        )

    def test_getstate_finish_event(self):
        event = MCOFinishEvent()
        self.assertFalse(event.__getstate__())

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
