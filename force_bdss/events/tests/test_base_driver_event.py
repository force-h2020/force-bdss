import unittest

from traits.api import Instance, Int

from force_bdss.core.data_value import DataValue
from force_bdss.events.base_driver_event import BaseDriverEvent


class DummyEvent(BaseDriverEvent):
    stateless_data = Int(1)
    stateful_data = Instance(DataValue)


class TestBaseDriverEvent(unittest.TestCase):

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
