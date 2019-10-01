from unittest import TestCase

import testfixtures

from force_bdss.app.evaluate_operation import EvaluateOperation
from force_bdss.tests import fixtures
from force_bdss.tests.probe_classes.workflow_file import (
    ProbeWorkflowFile
)


class TestEvaluateOperation(TestCase):

    def setUp(self):
        self.operation = EvaluateOperation()

    def test__init__(self):

        self.assertIsNone(self.operation.workflow_file)
        # workflow attribute delegates to workflow_file, so
        # should raise exception if not defined
        with self.assertRaises(AttributeError):
            self.assertIsNone(self.operation.workflow)

    def test_assign_workflow_file(self):

        self.operation.workflow_file = ProbeWorkflowFile()
        self.assertIsNone(self.operation.workflow)

        self.operation.workflow_file.path = fixtures.get("test_empty.json")
        self.operation.workflow_file.read()
        self.assertIsNotNone(self.operation.workflow)

    def test_run(self):
        self.operation.workflow_file = ProbeWorkflowFile(
            path=fixtures.get("test_empty.json")
        )
        self.operation.workflow_file.read()

        with testfixtures.LogCapture() as capture:
            self.operation.run()

            capture.check(
                ('force_bdss.app.evaluate_operation',
                 'INFO',
                 'No MCO defined. Nothing to do. Exiting.'),
            )