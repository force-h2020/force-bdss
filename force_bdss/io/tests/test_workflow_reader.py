from copy import deepcopy
import unittest
import logging

import testfixtures

from force_bdss.core.workflow import Workflow
from force_bdss.core.execution_layer import ExecutionLayer
from force_bdss.core.input_slot_info import InputSlotInfo
from force_bdss.core.output_slot_info import OutputSlotInfo
from force_bdss.io.workflow_reader import (
    WorkflowReader,
    InvalidVersionException,
    InvalidFileException,
    MissingPluginException,
    ModelInstantiationFailedException,
    deprecated_wf_format,
)
from force_bdss.tests.dummy_classes.factory_registry import (
    DummyFactoryRegistry,
)
from force_bdss.tests.probe_classes.factory_registry import (
    ProbeFactoryRegistry,
)
from force_bdss.tests import fixtures
from force_bdss.tests.dummy_classes.mco import DummyMCOParameter
from force_bdss.tests.dummy_classes.data_source import DummyDataSourceModel


log = logging.getLogger(__name__)


class TestWorkflowReader(unittest.TestCase):
    def setUp(self):
        self.registry = DummyFactoryRegistry()
        self.wfreader = WorkflowReader(self.registry)
        self.working_data = fixtures.get("test_workflow_reader.json")

    def test_load_data(self):
        data = self.wfreader.load_data(self.working_data)
        control_dict = {
            "version": "1.1",
            "workflow": {
                "mco_model": {
                    "id": "force.bdss.enthought.plugin.test."
                    "v0.factory.dummy_mco",
                    "model_data": {
                        "parameters": [
                            {
                                "id": "force.bdss.enthought.plugin."
                                "test.v0.factory.dummy_mco."
                                "parameter.dummy_mco_parameter",
                                "model_data": {},
                            }
                        ],
                        "kpis": [],
                    },
                },
                "notification_listeners": [
                    {
                        "id": "force.bdss.enthought.plugin.test.v0."
                        "factory.dummy_notification_listener",
                        "model_data": {},
                    }
                ],
                "execution_layers": [
                    {
                        "data_sources": [
                            {
                                "id": "force.bdss.enthought.plugin."
                                "test.v0.factory.dummy_data_source",
                                "model_data": {
                                    "input_slot_info": [
                                        {"name": "input_slot_name"}
                                    ],
                                    "output_slot_info": [
                                        {"name": "output_slot_name"}
                                    ],
                                },
                            }
                        ]
                    }
                ],
            },
        }

        self.assertDictEqual(data, control_dict)

    def test_read_version(self):
        json_data = self.wfreader.load_data(self.working_data)
        version = self.wfreader._extract_version(json_data)
        self.assertEqual("1.1", version)

    def test__extract_mco_model(self):
        json_data = self.wfreader.load_data(self.working_data)
        workflow_data = json_data["workflow"]
        mco_model = self.wfreader._extract_mco_model(workflow_data)

        mco_factory = self.registry.mco_factories[0]
        expected_mco_model = mco_factory.model_class
        self.assertIsInstance(mco_model, expected_mco_model)
        self.assertEqual(0, len(mco_model.kpis))
        self.assertEqual(1, len(mco_model.parameters))
        self.assertIsInstance(mco_model.parameters[0], DummyMCOParameter)

    def test__extract_execution_layers(self):
        json_data = self.wfreader.load_data(self.working_data)
        workflow_data = json_data["workflow"]
        self.wfreader.workflow_format_version = json_data["version"]

        exec_layers = self.wfreader._extract_execution_layers(workflow_data)
        self.assertEqual(1, len(exec_layers))
        self.assertIsInstance(exec_layers[0], ExecutionLayer)

        self.assertEqual(1, len(exec_layers[0].data_sources))
        data_source = exec_layers[0].data_sources[0]
        self.assertIsInstance(data_source, DummyDataSourceModel)

        input_slots = data_source.input_slot_info
        self.assertEqual(1, len(input_slots))
        self.assertIsInstance(input_slots[0], InputSlotInfo)
        self.assertEqual("input_slot_name", input_slots[0].name)

        output_slots = data_source.output_slot_info
        self.assertEqual(1, len(output_slots))
        self.assertIsInstance(output_slots[0], OutputSlotInfo)
        self.assertEqual("output_slot_name", output_slots[0].name)

    def test_initialization(self):
        self.assertEqual(self.wfreader.factory_registry, self.registry)

        workflow = self.wfreader.read(self.working_data)

        self.assertIsInstance(workflow, Workflow)

    def test_read_version_1(self):
        old_json = fixtures.get("test_workflow_reader_v1.json")
        self.wfreader.read(old_json)

    def test_invalid_version(self):
        data = {"version": "2", "workflow": {}}

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(InvalidVersionException):
                self.wfreader._extract_version(data)
            capture.check(
                (
                    "force_bdss.io.workflow_reader",
                    "ERROR",
                    "Invalid input file format: "
                    " version 2 is not in the "
                    "list of supported versions ['1', '1.1']",
                )
            )

        data = {"workflow": {}}
        with testfixtures.LogCapture() as capture:
            with self.assertRaises(InvalidFileException):
                self.wfreader._extract_version(data)
            capture.check(
                (
                    "force_bdss.io.workflow_reader",
                    "ERROR",
                    "Invalid input file format: " "no version specified",
                )
            )

        data = {}
        with testfixtures.LogCapture():
            with self.assertRaises(InvalidFileException):
                self.wfreader._extract_version(data)

    def test_missing_key(self):
        data = {"version": "1", "workflow": {}}

        with testfixtures.LogCapture():
            with self.assertRaises(InvalidFileException):
                self.wfreader._extract_workflow(data)

    def test_missing_plugin_mco(self):
        data = self.wfreader.load_data(self.working_data)
        data["workflow"]["mco_model"]["id"] = "missing_mco"

        with self.assertRaises(MissingPluginException):
            self.wfreader._extract_workflow(data)

    def test_missing_plugin_mco_parameter(self):
        data = self.wfreader.load_data(self.working_data)
        data["workflow"]["mco_model"]["model_data"]["parameters"][0][
            "id"
        ] = "missing_parameter"

        with self.assertRaises(MissingPluginException):
            self.wfreader._extract_workflow(data)

    def test_missing_plugin_notification_listener(self):
        data = self.wfreader.load_data(self.working_data)
        data["workflow"]["notification_listeners"][0]["id"] = "missing_nl"
        self.wfreader.workflow_format_version = data["version"]

        with self.assertRaises(MissingPluginException):
            self.wfreader._extract_workflow(data)

    def test_missing_plugin_data_source(self):
        data = self.wfreader.load_data(self.working_data)
        self.wfreader.workflow_format_version = data["version"]

        exec_layers = data["workflow"]["execution_layers"]
        exec_layers[0]["data_sources"][0]["id"] = "missing_ds"

        with self.assertRaises(MissingPluginException):
            self.wfreader._extract_workflow(data)

    def test_deprecated_wf_format_wrapper(self):
        data = self.wfreader.load_data(self.working_data)
        data["workflow"]["mco"] = data["workflow"].pop("mco_model")
        self.wfreader.workflow_format_version = data["version"]

        with testfixtures.LogCapture() as capture:
            self.wfreader._extract_mco_model(data["workflow"])
            expected_log = (
                "force_bdss.core.workflow",
                "WARNING",
                "The Workflow object format with 'mco' attribute is "
                "now deprecated. Please use 'mco_model' attribute instead.",
            )
            capture.check(expected_log)

    def test_persistent_wfdata(self):
        data = self.wfreader.load_data(self.working_data)
        self.wfreader.workflow_format_version = data["version"]

        workflow_data = data["workflow"]
        copied_data = deepcopy(workflow_data)

        self.wfreader._extract_mco_model(workflow_data)
        self.assertDictEqual(copied_data, workflow_data)
        self.wfreader._extract_mco_model(workflow_data)

        self.wfreader._extract_execution_layers(workflow_data)
        self.assertDictEqual(copied_data, workflow_data)
        self.wfreader._extract_execution_layers(workflow_data)

        self.wfreader._extract_notification_listeners(workflow_data)
        self.assertDictEqual(copied_data, workflow_data)
        self.wfreader._extract_notification_listeners(workflow_data)


class TestModelCreationFailure(unittest.TestCase):
    def setUp(self):
        self.registry = ProbeFactoryRegistry()
        self.wfreader = WorkflowReader(self.registry)
        self.working_data = fixtures.get("test_failing_workflow_reader.json")

    def test_basic_probe_loading(self):
        self.wfreader.read(self.working_data)

    def test_data_source_model_throws(self):
        self.registry.data_source_factories[0].raises_on_create_model = True
        with testfixtures.LogCapture():
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader.read(self.working_data)

    def test_mco_model_throws(self):
        self.registry.mco_factories[0].raises_on_create_model = True
        with testfixtures.LogCapture():
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader.read(self.working_data)

    def test_notification_listener_throws(self):
        factory = self.registry.notification_listener_factories[0]
        factory.raises_on_create_model = True

        with testfixtures.LogCapture():
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader.read(self.working_data)

    def test__extract_mco_parameters_throws(self):
        wfdata = self.wfreader.load_data(self.working_data)["workflow"]
        model_data = wfdata["mco_model"]["model_data"]
        model_data["parameters"][0]["model_data"] = {"bad": "data"}
        with testfixtures.LogCapture() as capture:
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader._extract_mco_model(wfdata)
            capture.check(
                (
                    "force_bdss.io.workflow_reader",
                    "ERROR",
                    "Unable to create model for MCO force.bdss.enthought."
                    "plugin.test.v0.factory.probe_mco parameter force."
                    "bdss.enthought.plugin.test.v0.factory.probe_mco."
                    "parameter.probe_mco_parameter: Cannot set the undefined "
                    "'bad' attribute of a 'ProbeParameter' object. This is "
                    "likely due to an error "
                    "in the plugin. Check the logs for more information.",
                )
            )


class TestDeprecationWrapper(unittest.TestCase):
    def test_wrapper(self):
        @deprecated_wf_format
        def decorated_method(self_reference, data_dict):
            return data_dict

        expected_log = (
            "force_bdss.core.workflow",
            "WARNING",
            "The Workflow object format with 'mco' attribute is "
            "now deprecated. Please use 'mco_model' attribute instead.",
        )
        mco_dict = {"mco": 1}
        mco_model_dict = {"mco_model": 1}
        mixed_dict = {"mco": 1, "mco_model": 1}
        with testfixtures.LogCapture() as capture:
            self.assertDictEqual(
                decorated_method(None, mco_dict), mco_model_dict
            )
            capture.check(expected_log)

        with testfixtures.LogCapture() as capture:
            self.assertDictEqual(
                decorated_method(None, mco_model_dict), mco_model_dict
            )
            capture.check()

        with testfixtures.LogCapture() as capture:
            self.assertDictEqual(
                decorated_method(None, mixed_dict), mixed_dict
            )
            capture.check()
