import json
import unittest
from six import StringIO

from force_bdss.factory_registry_plugin import FactoryRegistryPlugin
from force_bdss.io.workflow_reader import (
    WorkflowReader,
    InvalidVersionException, InvalidFileException)

try:
    import mock
except ImportError:
    from unittest import mock


class TestWorkflowReader(unittest.TestCase):
    def setUp(self):
        self.mock_factory_registry = mock.Mock(spec=FactoryRegistryPlugin)

        self.wfreader = WorkflowReader(self.mock_factory_registry)

    def test_initialization(self):
        self.assertEqual(self.wfreader.factory_registry,
                         self.mock_factory_registry)

    def test_invalid_version(self):
        data = {
            "version": "2",
            "workflow": {}
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
