import json
from unittest import TestCase

import testfixtures

from traits.testing.unittest_tools import UnittestTools

from force_bdss.core.data_value import DataValue
from force_bdss.core.execution_layer import ExecutionLayer, _bind_data_values
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.core.slot import Slot
from force_bdss.tests.probe_classes.factory_registry import (
    ProbeFactoryRegistry,
)
from force_bdss.events.base_driver_event import BaseDriverEvent
from force_bdss.tests import fixtures


class TestExecutionLayer(TestCase, UnittestTools):
    def setUp(self):
        self.registry = ProbeFactoryRegistry()
        self.plugin = self.registry.plugin

        factory = self.registry.data_source_factories[0]
        self.layer = ExecutionLayer(
            data_sources=[factory.create_model(), factory.create_model()]
        )

    def test__init__(self):
        self.assertEqual(2, len(self.layer.data_sources))

    def test_verify(self):

        errors = self.layer.verify()
        messages = [error.local_error for error in errors]

        self.assertEqual(4, len(messages))
        self.assertIn("The number of input slots is incorrect.", messages)
        self.assertIn("The number of output slots is incorrect.", messages)

        self.layer.data_sources = []
        errors = self.layer.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(1, len(messages))
        self.assertIn("Layer has no data sources", messages)

    def test_create_data_source_error(self):

        factory = self.registry.data_source_factories[0]
        factory.raises_on_create_data_source = True

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(Exception):
                self.layer.execute_layer([])
            capture.check(
                (
                    "force_bdss.core.execution_layer",
                    "ERROR",
                    "Unable to create data source from factory "
                    "'force.bdss.enthought.plugin.test.v0.factory."
                    "probe_data_source' in plugin "
                    "'force.bdss.enthought.plugin.test.v0'."
                    " This may indicate a programming "
                    "error in the plugin",
                )
            )

    def test_data_source_run_error(self):

        data_values = [DataValue(name="foo")]
        self.layer.data_sources[0].input_slot_info = [
            InputSlotInfo(name="foo")
        ]

        factory = self.registry.data_source_factories[0]
        factory.raises_on_data_source_run = True

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(Exception):
                self.layer.execute_layer(data_values)
            capture.check(
                (
                    "force_bdss.core.execution_layer",
                    "INFO",
                    "Evaluating for Data Source test_data_source",
                ),
                ("force_bdss.core.execution_layer", "INFO", "Passed values:"),
                (
                    "force_bdss.core.execution_layer",
                    "INFO",
                    "0:  foo = None (AVERAGE)",
                ),
                (
                    "force_bdss.core.execution_layer",
                    "ERROR",
                    "Evaluation could not be performed. "
                    "Run method raised exception.",
                ),
            )

    def test_error_for_incorrect_return_type(self):

        data_values = [DataValue(name="foo")]
        self.layer.data_sources[0].input_slot_info = [
            InputSlotInfo(name="foo")
        ]

        def probe_run(self, *args, **kwargs):
            return "hello"

        factory = self.registry.data_source_factories[0]
        factory.run_function = probe_run

        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                RuntimeError,
                "The run method of data source "
                "test_data_source must return a list. It "
                r"returned instead <.* 'str'>. Fix the run\(\)"
                " method to return the appropriate entity.",
            ):
                self.layer.execute_layer(data_values)

    def test_error_for_output_slots(self):
        data_values = [DataValue(name="foo")]
        self.layer.data_sources[0].input_slot_info = [
            InputSlotInfo(name="foo")
        ]

        def probe_run(self, *args, **kwargs):
            return ["too", "many", "data", "values"]

        factory = self.registry.data_source_factories[0]
        factory.run_function = probe_run

        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                RuntimeError,
                r"The number of data values \(4 values\) returned"
                " by 'test_data_source' does not match the number"
                r" of output slots it specifies \(1 values\)."
                " This is likely a plugin error.",
            ):
                self.layer.execute_layer(data_values)

    def test_error_for_output_slot_info(self):
        data_values = [DataValue(name="foo")]
        self.layer.data_sources[0].input_slot_info = [
            InputSlotInfo(name="foo")
        ]
        self.layer.data_sources[0].output_slot_info = [
            OutputSlotInfo(name="one"),
            OutputSlotInfo(name="too_many"),
        ]

        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                RuntimeError,
                r"The number of data values \(1 values\) returned"
                " by 'test_data_source' does not match the number"
                r" of user-defined names specified \(2 values\)."
                " This is either a plugin error or a file"
                " error.",
            ):
                self.layer.execute_layer(data_values)

    def test_error_for_non_data_source(self):

        data_values = [DataValue(name="foo")]
        self.layer.data_sources[0].input_slot_info = [
            InputSlotInfo(name="foo")
        ]
        self.layer.data_sources[0].output_slot_info = [
            OutputSlotInfo(name="one")
        ]

        def probe_run(self, *args, **kwargs):
            return ["hello"]

        factory = self.registry.data_source_factories[0]
        factory.run_function = probe_run

        with testfixtures.LogCapture():
            with self.assertRaisesRegex(
                RuntimeError,
                "The result list returned by DataSource "
                "test_data_source"
                " contains an entry that is not a DataValue."
                " An entry of type <.* 'str'> was instead found"
                " in position 0."
                r" Fix the DataSource.run\(\) method to"
                " return the appropriate entity.",
            ):
                self.layer.execute_layer(data_values)

    def test_execute_layer_results(self):

        data_values = [
            DataValue(name="foo"),
            DataValue(name="bar"),
            DataValue(name="baz"),
            DataValue(name="quux"),
        ]

        def run(self, *args, **kwargs):
            return [DataValue(value=1), DataValue(value=2), DataValue(value=3)]

        ds_factory = self.registry.data_source_factories[0]
        ds_factory.input_slots_size = 2
        ds_factory.output_slots_size = 3
        ds_factory.run_function = run
        evaluator_model = ds_factory.create_model()

        evaluator_model.input_slot_info = [
            InputSlotInfo(name="foo"),
            InputSlotInfo(name="quux"),
        ]
        evaluator_model.output_slot_info = [
            OutputSlotInfo(name="one"),
            OutputSlotInfo(name=""),
            OutputSlotInfo(name="three"),
        ]

        self.layer.data_sources = [evaluator_model]
        res = self.layer.execute_layer(data_values)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].name, "one")
        self.assertEqual(res[0].value, 1)
        self.assertEqual(res[1].name, "three")
        self.assertEqual(res[1].value, 3)

    def test_from_json(self):
        json_path = fixtures.get("test_probe.json")
        with open(json_path) as f:
            data = json.load(f)
        layer_data = {"data_sources": data["workflow"]["execution_layers"][0]}
        layer = ExecutionLayer.from_json(self.registry, layer_data)

        self.assertDictEqual(
            layer_data["data_sources"][0],
            {
                "id": "force.bdss.enthought.plugin.test.v0."
                "factory.probe_data_source",
                "model_data": {
                    "input_slot_info": [
                        {"source": "Environment", "name": "foo"}
                    ],
                    "output_slot_info": [{"name": "bar"}],
                },
            },
        )

        layer_data["data_sources"][0]["model_data"].update(
            {
                "input_slots_type": "PRESSURE",
                "output_slots_type": "PRESSURE",
                "input_slots_size": 1,
                "output_slots_size": 1,
            }
        )
        self.assertDictEqual(
            layer.__getstate__(), layer_data
        )

    def test_empty_layer_from_json(self):
        layer = ExecutionLayer.from_json(self.registry, {})
        self.assertEqual(0, len(layer.data_sources))

    def test_notify_driver_event(self):
        with self.assertTraitChanges(
                self.layer, 'event', count=1):
            self.layer.data_sources[0].notify(BaseDriverEvent())


class TestBindDataValues(TestCase):
    def setUp(self):
        self.registry = ProbeFactoryRegistry()
        self.plugin = self.registry.plugin

        self.data_values = [
            DataValue(name="foo"),
            DataValue(name="bar"),
            DataValue(name="baz"),
        ]

        self.slot_map = (InputSlotInfo(name="baz"), InputSlotInfo(name="bar"))

        self.slots = (Slot(), Slot())

    def test_bind_data_values_slots_error(self):

        with self.assertRaisesRegex(
            RuntimeError,
            "The length of the slots is not equal to the"
            " length of the slot map. This may indicate "
            "a file error.",
        ):
            _bind_data_values(self.data_values, self.slot_map, [])

    def test_bind_data_values_name_error(self):
        with self.assertRaisesRegex(
            RuntimeError,
            "Unable to find requested name 'baz' in available "
            "data values. ",
        ):
            _bind_data_values(self.data_values[:-1], self.slot_map, self.slots)

    def test_bind_data_values(self):

        result = _bind_data_values(self.data_values, self.slot_map, self.slots)
        self.assertEqual(result[0], self.data_values[2])
        self.assertEqual(result[1], self.data_values[1])
