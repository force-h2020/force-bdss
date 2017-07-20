import json
import unittest
from six import StringIO

from force_bdss.bundle_registry_plugin import BundleRegistryPlugin
from force_bdss.io.workflow_reader import (
    WorkflowReader,
    InvalidVersionException, InvalidFileException)

try:
    import mock
except ImportError:
    from unittest import mock


class TestWorkflowReader(unittest.TestCase):
    def setUp(self):
        self.mock_bundle_registry = mock.Mock(spec=BundleRegistryPlugin)
        self.wfreader = WorkflowReader(self.mock_bundle_registry)

    def test_initialization(self):
        self.assertEqual(self.wfreader.bundle_registry,
                         self.mock_bundle_registry)

    def test_invalid_version(self):
        data = {
            "version": "2"
        }

        with self.assertRaises(InvalidVersionException):
            self.wfreader.read(self._as_json_stringio(data))

    def test_absent_version(self):
        data = {
        }

        with self.assertRaises(InvalidFileException):
            self.wfreader.read(self._as_json_stringio(data))

    def _as_json_stringio(self, data):
        fp = StringIO()
        json.dump(data, fp)
        fp.seek(0)

        return fp
