import json
import unittest
from six import StringIO

import testfixtures

from force_bdss.io.workflow_reader import (
    WorkflowReader,
    InvalidVersionException, InvalidFileException)
from force_bdss.tests.dummy_classes.factory_registry_plugin import \
    DummyFactoryRegistryPlugin

try:
    import mock
except ImportError:
    from unittest import mock


class TestWorkflowReader(unittest.TestCase):
    def setUp(self):
        self.registry = DummyFactoryRegistryPlugin()

        self.wfreader = WorkflowReader(self.registry)

    def test_initialization(self):
        self.assertEqual(self.wfreader.factory_registry,
                         self.registry)

    def test_invalid_version(self):
        data = {
            "version": "2",
            "workflow": {}
        }

        with testfixtures.LogCapture():
            with self.assertRaises(InvalidVersionException):
                self.wfreader.read(self._as_json_stringio(data))

    def test_absent_version(self):
        data = {
        }

        with testfixtures.LogCapture():
            with self.assertRaises(InvalidFileException):
                self.wfreader.read(self._as_json_stringio(data))

    def test_missing_key(self):
        data = {
            "version": "1",
            "workflow": {}
        }

        with testfixtures.LogCapture():
            with self.assertRaises(InvalidFileException):
                self.wfreader.read(self._as_json_stringio(data))

    def _as_json_stringio(self, data):
        fp = StringIO()
        json.dump(data, fp)
        fp.seek(0)

        return fp
