from unittest import TestCase

from force_bdss.tests import fixtures
from force_bdss.tests.probe_classes.workflow_file import (
    ProbeWorkflowFile
)


class TestWorkflowFile(TestCase):

    def setUp(self):

        self.workflow_file = ProbeWorkflowFile(
            path='foo/bar'
        )

    def test__init__(self):
        self.assertIsNone(self.workflow_file.workflow)
        self.assertEqual('foo/bar', self.workflow_file.path)

    def test_read(self):
        self.workflow_file.path = fixtures.get("test_empty.json")
        self.workflow_file.read()
        self.assertIsNotNone(self.workflow_file.workflow)
