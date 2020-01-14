from copy import deepcopy
import json
import unittest
from io import StringIO
import logging

import testfixtures

from force_bdss.core.workflow import Workflow
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

log = logging.getLogger(__name__)


class TestWorkflowReader(unittest.TestCase):
    def setUp(self):
        self.registry = DummyFactoryRegistry()
        self.wfreader = WorkflowReader(self.registry)

        self.working_data = {
            "version": "1",
            "workflow": {
                "mco_model": {
                    "id": "force.bdss.enthought.plugin.test.v0"
                    ".factory.dummy_mco",
                    "model_data": {
                        "parameters": [
                            {
                                "id": "force.bdss.enthought.plugin.test.v0"
                                ".factory.dummy_mco.parameter"
                                ".dummy_mco_parameter",
                                "model_data": {},
                            }
                        ],
                        "kpis": [],
                    },
                },
                "execution_layers": [
                    [
                        {
                            "id": "force.bdss.enthought.plugin.test.v0"
                            ".factory.dummy_data_source",
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
                ],
                "notification_listeners": [
                    {
                        "id": "force.bdss.enthought.plugin.test.v0"
                        ".factory.dummy_notification_listener",
                        "model_data": {},
                    }
                ],
            },
        }

    def test_initialization(self):
        self.assertEqual(self.wfreader.factory_registry, self.registry)

        workflow = self.wfreader.read(_as_json_stringio(self.working_data))

        self.assertIsInstance(workflow, Workflow)

    def test_invalid_version(self):
        data = {"version": "2", "workflow": {}}

        with testfixtures.LogCapture():
            with self.assertRaises(InvalidVersionException):
                self.wfreader.read(_as_json_stringio(data))

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(InvalidVersionException):
                self.wfreader._extract_version(data)
            capture.check(
                (
                    "force_bdss.io.workflow_reader",
                    "ERROR",
                    "Invalid input file format: "
                    " version 2 is not in the "
                    "list of supported versions ['1']",
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
                    "Invalid input file format: "
                    "no version specified",
                )
            )

    def test_absent_version(self):
        data = {}

        with testfixtures.LogCapture():
            with self.assertRaises(InvalidFileException):
                self.wfreader.read(_as_json_stringio(data))

    def test_missing_key(self):
        data = {"version": "1", "workflow": {}}

        with testfixtures.LogCapture():
            with self.assertRaises(InvalidFileException):
                self.wfreader.read(_as_json_stringio(data))

    def test_missing_plugin_mco(self):
        data = self.working_data
        data["workflow"]["mco_model"]["id"] = "missing_mco"

        with self.assertRaises(MissingPluginException):
            self.wfreader.read(_as_json_stringio(data))

    def test_missing_plugin_mco_parameter(self):
        data = self.working_data
        data["workflow"]["mco_model"]["model_data"]["parameters"][0][
            "id"
        ] = "missing_parameter"

        with self.assertRaises(MissingPluginException):
            self.wfreader.read(_as_json_stringio(data))

    def test_missing_plugin_notification_listener(self):
        data = self.working_data
        data["workflow"]["notification_listeners"][0]["id"] = "missing_nl"

        with self.assertRaises(MissingPluginException):
            self.wfreader.read(_as_json_stringio(data))

    def test_missing_plugin_data_source(self):
        data = self.working_data
        data["workflow"]["execution_layers"][0][0]["id"] = "missing_ds"

        with self.assertRaises(MissingPluginException):
            self.wfreader.read(_as_json_stringio(data))

    def test_deprecated_wf_format_wrapper(self):
        self.working_data["workflow"]["mco"] = self.working_data[
            "workflow"
        ].pop("mco_model")

        with testfixtures.LogCapture() as capture:
            self.wfreader._extract_mco_model(self.working_data["workflow"])
            expected_log = (
                "force_bdss.core.workflow",
                "WARNING",
                "The Workflow object format with 'mco' attribute is "
                "now deprecated. Please use 'mco_model' attribute instead.",
            )
            capture.check(expected_log)

    def test_persistent_wfdata(self):
        copied_data = deepcopy(self.working_data["workflow"])
        self.wfreader._extract_mco_model(self.working_data["workflow"])
        self.assertDictEqual(copied_data, self.working_data["workflow"])
        self.wfreader._extract_mco_model(self.working_data["workflow"])

        self.wfreader._extract_execution_layers(self.working_data["workflow"])
        self.assertDictEqual(copied_data, self.working_data["workflow"])
        self.wfreader._extract_execution_layers(self.working_data["workflow"])

        self.wfreader._extract_notification_listeners(
            self.working_data["workflow"]
        )
        self.assertDictEqual(copied_data, self.working_data["workflow"])
        self.wfreader._extract_notification_listeners(
            self.working_data["workflow"]
        )


class TestModelCreationFailure(unittest.TestCase):
    def setUp(self):
        self.registry = ProbeFactoryRegistry()
        self.wfreader = WorkflowReader(self.registry)

        self.working_data = {
            "version": "1",
            "workflow": {
                "mco_model": {
                    "id": "force.bdss.enthought.plugin.test.v0"
                    ".factory.probe_mco",
                    "model_data": {
                        "parameters": [
                            {
                                "id": "force.bdss.enthought.plugin.test.v0"
                                ".factory.probe_mco.parameter"
                                ".probe_mco_parameter",
                                "model_data": {},
                            }
                        ],
                        "kpis": [],
                    },
                },
                "execution_layers": [
                    [
                        {
                            "id": "force.bdss.enthought.plugin.test.v0"
                            ".factory.probe_data_source",
                            "model_data": {
                                "input_slot_info": [],
                                "output_slot_info": [],
                            },
                        }
                    ]
                ],
                "notification_listeners": [
                    {
                        "id": "force.bdss.enthought.plugin.test.v0"
                        ".factory.probe_notification_listener",
                        "model_data": {},
                    }
                ],
            },
        }

    def test_basic_probe_loading(self):
        self.wfreader.read(_as_json_stringio(self.working_data))

    def test_data_source_model_throws(self):
        self.registry.data_source_factories[0].raises_on_create_model = True
        with testfixtures.LogCapture():
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader.read(_as_json_stringio(self.working_data))

    def test_mco_model_throws(self):
        self.registry.mco_factories[0].raises_on_create_model = True
        with testfixtures.LogCapture():
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader.read(_as_json_stringio(self.working_data))

    def test_notification_listener_throws(self):
        factory = self.registry.notification_listener_factories[0]
        factory.raises_on_create_model = True

        with testfixtures.LogCapture():
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader.read(_as_json_stringio(self.working_data))

    def test__extract_mco_parameters_throws(self):
        model_data = self.working_data["workflow"]["mco_model"]["model_data"]
        model_data["parameters"][0]["model_data"] = {"bad": "data"}
        with testfixtures.LogCapture() as capture:
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader.read(_as_json_stringio(self.working_data))
            capture.check(
                (
                    "force_bdss.io.workflow_reader",
                    "ERROR",
                    "Unable to create model for MCO force.bdss.enthought."
                    "plugin.test.v0.factory.probe_mco parameter force."
                    "bdss.enthought.plugin.test.v0.factory.probe_mco."
                    "parameter.probe_mco_parameter : Cannot set the undefined "
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


def _as_json_stringio(data):
    fp = StringIO()
    json.dump(data, fp)
    fp.seek(0)

    return fp
