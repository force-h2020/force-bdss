import json
import unittest
from six import StringIO

import testfixtures

from force_bdss.core.workflow import Workflow
from force_bdss.io.workflow_reader import (
    WorkflowReader,
    InvalidVersionException, InvalidFileException, MissingPluginException,
    ModelInstantiationFailedException)
from force_bdss.tests.dummy_classes.factory_registry_plugin import \
    DummyFactoryRegistryPlugin
from force_bdss.tests.probe_classes.factory_registry_plugin import \
    ProbeFactoryRegistryPlugin


class TestWorkflowReader(unittest.TestCase):
    def setUp(self):
        self.registry = DummyFactoryRegistryPlugin()
        self.wfreader = WorkflowReader(self.registry)

        self.working_data = {
            "version": "1",
            "workflow": {
                "mco": {
                    "id": "force.bdss.enthought.plugin.test.v0"
                          ".factory.dummy_mco",
                    "model_data": {
                        "parameters": [
                            {
                                "id": "force.bdss.enthought.plugin.test.v0"
                                      ".factory.dummy_mco.parameter"
                                      ".dummy_mco_parameter",
                                "model_data": {}
                            }
                        ]
                    },
                },
                "execution_layers": [
                    [{
                        "id": "force.bdss.enthought.plugin.test.v0"
                              ".factory.dummy_data_source",
                        "model_data": {
                            "input_slot_info": [],
                            "output_slot_info": [],
                        }
                    }],
                ],
                "notification_listeners": [
                    {
                        "id": "force.bdss.enthought.plugin.test.v0"
                              ".factory.dummy_notification_listener",
                        "model_data": {}
                    },
                ]
            }
        }

    def test_initialization(self):
        self.assertEqual(self.wfreader.factory_registry,
                         self.registry)

        workflow = self.wfreader.read(
            _as_json_stringio(self.working_data)
        )

        self.assertIsInstance(workflow, Workflow)

    def test_invalid_version(self):
        data = {
            "version": "2",
            "workflow": {}
        }

        with testfixtures.LogCapture():
            with self.assertRaises(InvalidVersionException):
                self.wfreader.read(_as_json_stringio(data))

    def test_absent_version(self):
        data = {
        }

        with testfixtures.LogCapture():
            with self.assertRaises(InvalidFileException):
                self.wfreader.read(_as_json_stringio(data))

    def test_missing_key(self):
        data = {
            "version": "1",
            "workflow": {}
        }

        with testfixtures.LogCapture():
            with self.assertRaises(InvalidFileException):
                self.wfreader.read(_as_json_stringio(data))

    def test_missing_plugin_mco(self):
        data = self.working_data
        data["workflow"]["mco"]["id"] = "missing_mco"

        with self.assertRaises(MissingPluginException):
            self.wfreader.read(_as_json_stringio(data))

    def test_missing_plugin_mco_parameter(self):
        data = self.working_data
        data["workflow"]["mco"]["model_data"]["parameters"][0]["id"] = \
            "missing_parameter"

        with self.assertRaises(MissingPluginException):
            self.wfreader.read(_as_json_stringio(data))

    def test_missing_plugin_notification_listener(self):
        data = self.working_data
        data["workflow"]["notification_listeners"][0]["id"] = \
            "missing_nl"

        with self.assertRaises(MissingPluginException):
            self.wfreader.read(_as_json_stringio(data))

    def test_missing_plugin_data_source(self):
        data = self.working_data
        data["workflow"]["execution_layers"][0][0]["id"] = \
            "missing_ds"

        with self.assertRaises(MissingPluginException):
            self.wfreader.read(_as_json_stringio(data))


class TestModelCreationFailure(unittest.TestCase):
    def setUp(self):
        self.registry = ProbeFactoryRegistryPlugin()
        self.wfreader = WorkflowReader(self.registry)

        self.working_data = {
            "version": "1",
            "workflow": {
                "mco": {
                    "id": "force.bdss.enthought.plugin.test.v0"
                          ".factory.probe_mco",
                    "model_data": {
                        "parameters": [
                            {
                                "id": "force.bdss.enthought.plugin.test.v0"
                                      ".factory.probe_mco.parameter"
                                      ".probe_mco_parameter",
                                "model_data": {}
                            }
                        ]
                    },
                },
                "execution_layers": [
                    [{
                        "id": "force.bdss.enthought.plugin.test.v0"
                              ".factory.probe_data_source",
                        "model_data": {
                            "input_slot_info": [],
                            "output_slot_info": [],
                        }
                    }],
                ],
                "notification_listeners": [
                    {
                        "id": "force.bdss.enthought.plugin.test.v0"
                              ".factory.probe_notification_listener",
                        "model_data": {}
                    },
                ]
            }
        }

    def test_basic_probe_loading(self):
        self.wfreader.read(
            _as_json_stringio(self.working_data)
        )

    def test_data_source_model_throws(self):
        self.registry.data_source_factories[0].raises_on_create_model = True
        with testfixtures.LogCapture():
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader.read(
                    _as_json_stringio(self.working_data)
                )

    def test_mco_model_throws(self):
        self.registry.mco_factories[0].raises_on_create_model = True
        with testfixtures.LogCapture():
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader.read(
                    _as_json_stringio(self.working_data)
                )

    def test_notification_listener_throws(self):
        factory = self.registry.notification_listener_factories[0]
        factory.raises_on_create_model = True

        with testfixtures.LogCapture():
            with self.assertRaises(ModelInstantiationFailedException):
                self.wfreader.read(
                    _as_json_stringio(self.working_data)
                )


def _as_json_stringio(data):
    fp = StringIO()
    json.dump(data, fp)
    fp.seek(0)

    return fp
