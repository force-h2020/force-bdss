import unittest

from traits.api import Instance, Int

from force_bdss.core.data_value import DataValue
from force_bdss.core_driver_events import (
    MCOProgressEvent,
    WeightedMCOProgressEvent,
    MCOStartEvent,
    MCOFinishEvent,
    BaseDriverEvent,
)


class DummyEvent(BaseDriverEvent):
    stateless_data = Int(1)
    stateful_data = Instance(DataValue)


class TestCoreDriverEvents(unittest.TestCase):
    def test_getstate_progress_event(self):
        ev = MCOProgressEvent(
            optimal_kpis=[DataValue(value=10)],
            optimal_point=[DataValue(value=12), DataValue(value=13)]
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
                ]
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

    def test_getstate_base_event(self):
        event = BaseDriverEvent()
        self.assertFalse(event.__getstate__())

        event = DummyEvent(stateful_data=DataValue(value=1))
        self.assertDictEqual(
            event.__getstate__(),
            {
                "stateless_data": 1,
                "stateful_data": {
                    "accuracy": None,
                    "name": "",
                    "quality": "AVERAGE",
                    "type": "",
                    "value": 1,
                },
            },
        )

    def test_serialize_start_event(self):
        event = MCOStartEvent(
            parameter_names=["p1", "p2"], kpi_names=["k1", "k2", "k3"]
        )
        self.assertListEqual(event.serialize(), ["p1", "p2", "k1", "k2", "k3"])

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

        self.assertListEqual(event.serialize(), [12, 13, 10, 1.0])
