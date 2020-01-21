import unittest
import logging

import testfixtures

from force_bdss.core.workflow import Workflow
from force_bdss.io.workflow_reader import (
    WorkflowReader,
    InvalidVersionException,
    InvalidFileException,
)
from force_bdss.tests.dummy_classes.factory_registry import (
    DummyFactoryRegistry,
)
from force_bdss.tests import fixtures


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

    def test_initialization(self):
        self.assertEqual(self.wfreader.factory_registry, self.registry)

        workflow = self.wfreader.read(self.working_data)

        self.assertIsInstance(workflow, Workflow)

    def test_read_version_1(self):
        old_json = fixtures.get("test_workflow_reader_v1.json")
        workflow = self.wfreader.read(old_json)
        self.assertEqual(1, len(workflow.execution_layers))
        self.assertEqual(1, len(workflow.execution_layers[0].data_sources))

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
