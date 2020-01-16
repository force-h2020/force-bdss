from unittest import TestCase

from force_bdss.core.workflow import Workflow
from force_bdss.tests import fixtures
from force_bdss.tests.probe_classes.workflow_file import ProbeWorkflowFile


class TestWorkflowFile(TestCase):
    def setUp(self):

        self.workflow_file = ProbeWorkflowFile(path="foo/bar")

    def test__init__(self):
        self.assertIsNone(self.workflow_file.workflow)
        self.assertIsNotNone(self.workflow_file.reader)
        self.assertIsNotNone(self.workflow_file.writer)
        self.assertEqual("foo/bar", self.workflow_file.path)

    def test_from_path_classmethod(self):
        # Test normal behaviour
        workflow_file = ProbeWorkflowFile.from_path(
            path=fixtures.get("test_empty.json")
        )
        self.assertIsInstance(workflow_file, ProbeWorkflowFile)

    def test_read(self):
        # Test normal behaviour
        self.workflow_file.path = fixtures.get("test_empty.json")
        self.workflow_file.read()
        self.assertIsInstance(self.workflow_file.workflow, Workflow)

        # Test non-existent file
        self.workflow_file.path = "foo/bar"
        with self.assertRaisesRegex(
            FileNotFoundError, "No such file or directory: 'foo/bar'"
        ):
            self.workflow_file.read()

        # Test undefined reader
        self.workflow_file.reader = None
        with self.assertRaisesRegex(
            ValueError, "No workflow reader specified."
        ):
            self.workflow_file.read()

    def test_write(self):
        # Test normal behaviour
        self.workflow_file.path = fixtures.get("test_empty.json")
        self.workflow_file.read()
        self.workflow_file.write()

        # Test undefined writer
        self.workflow_file.writer = None
        with self.assertRaisesRegex(
            ValueError, "No workflow writer specified."
        ):
            self.workflow_file.write()
