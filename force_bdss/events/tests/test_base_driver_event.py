import unittest

from traits.api import Instance, Int

from force_bdss.core.data_value import DataValue
from force_bdss.events.base_driver_event import (
    BaseDriverEvent,
    DriverEventTypeError,
    DriverEventDeserializationError,
)


class DummyEvent(BaseDriverEvent):
    stateless_data = Int(1)
    stateful_data = Instance(DataValue)


class TestBaseDriverEvent(unittest.TestCase):

    def test_getstate_base_event(self):
        event = BaseDriverEvent()
        self.assertDictEqual(
            event.__getstate__(),
            {
                "id": "force_bdss.events.base_driver_event.BaseDriverEvent",
                "model_data": {},
            },
        )

        event = DummyEvent(stateful_data=DataValue(value=1))
        self.assertDictEqual(
            event.__getstate__(),
            {
                "id": "force_bdss.events.tests"
                      ".test_base_driver_event.DummyEvent",
                "model_data": {
                    "stateless_data": 1,
                    "stateful_data": {
                        "accuracy": None,
                        "name": "",
                        "quality": "AVERAGE",
                        "type": "",
                        "value": 1,
                    },
                },
            },
        )

    def test_get_event_class(self):
        data = {
            "id": "force_bdss.events.base_driver_event.BaseDriverEvent",
            "model_data": {},
        }
        klass = BaseDriverEvent.get_event_class(data["id"])
        self.assertIs(klass, BaseDriverEvent)

        data = {"id": "force_bdss.mco.base_mco.BaseMCO", "model_data": {}}
        error_message = (
            "Class <class 'force_bdss.mco.base_mco.BaseMCO'> "
            "must be a subclass of BaseDriverEvent"
        )
        with self.assertRaisesRegex(DriverEventTypeError, error_message):
            BaseDriverEvent.get_event_class(data["id"])

        data = {"id": "force_bdss.mco.base_mco.RandomClass", "model_data": {}}
        with self.assertRaisesRegex(
            ImportError,
            "Unable to locate the class definition RandomClass in module "
            "<.*> "
            f"requested by the event with id {data['id']}",
        ):
            BaseDriverEvent.get_event_class(data["id"])

    def test_from_json(self):
        data = {
            "id": "force_bdss.events.base_driver_event.BaseDriverEvent",
            "model_data": {},
        }
        event = BaseDriverEvent.from_json(data)
        self.assertIsInstance(event, BaseDriverEvent)
        self.assertDictEqual(event.__getstate__(), data)

    def test_raises_from_json(self):

        key_failed_data = {
            "model_data": {
                "some_key": [{"random_trait": "some data"}],
                "another_key": [],
            }
        }
        with self.assertRaisesRegex(
            DriverEventDeserializationError,
            "Could not parse json data. "
            "The `json_data` argument should contain the"
            "class id key 'id'.",
        ):
            BaseDriverEvent.from_json(key_failed_data)

    def test_loads_json_error(self):

        wrong_json_data = "something weird"
        with self.assertRaisesRegex(
            DriverEventDeserializationError,
            f"Data object {wrong_json_data} is not compatible "
            f"with the json.loads method and raises",
        ):
            BaseDriverEvent.loads_json(wrong_json_data)
