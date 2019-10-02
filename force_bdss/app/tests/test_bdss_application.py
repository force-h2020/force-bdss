import unittest
import warnings

import testfixtures

from traits.etsconfig.api import ETSConfig

from force_bdss.app.bdss_application import (
    BDSSApplication, _load_failure_callback, _import_extensions
)
from force_bdss.app.optimize_operation import OptimizeOperation
from force_bdss.core.workflow import Workflow
from force_bdss.tests import fixtures

from unittest import mock


def clear_toolkit():
    # note, this won't unimport any toolkit backends
    ETSConfig._toolkit = None


class TestBDSSApplication(unittest.TestCase):

    def setUp(self):
        self.addCleanup(clear_toolkit)

    def test_initialization(self):
        with testfixtures.LogCapture():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                app = BDSSApplication(False, "foo/bar")
        self.assertIsInstance(app.operation, OptimizeOperation)
        self.assertEqual(app.workflow_file.path, "foo/bar")
        self.assertEqual(ETSConfig.toolkit, 'null')

    def test_toolkit(self):
        ETSConfig.toolkit = 'dummy'
        with testfixtures.LogCapture():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                BDSSApplication(False, "foo/bar")
        self.assertEqual(ETSConfig.toolkit, 'dummy')

    def test_toolkit_null(self):
        ETSConfig.toolkit = 'null'
        with testfixtures.LogCapture():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                BDSSApplication(False, "foo/bar")
        self.assertEqual(ETSConfig.toolkit, 'null')

    def test_extension_load_failure(self):
        plugins = []
        with testfixtures.LogCapture() as log:
            _load_failure_callback(plugins,
                                   mock.Mock(),
                                   "foo",
                                   Exception("hello"))

        log.check(
            ('force_bdss.app.bdss_application',
             'ERROR',
             "Unable to load plugin foo. Exception: "
             "Exception. Message: hello"),
        )
        self.assertEqual(plugins, [])

    def test_import_extension(self):
        plugins = []
        plugin = mock.Mock()
        ext = mock.Mock()
        ext.obj = plugin
        _import_extensions(plugins, ext)

        self.assertEqual(plugins[0], plugin)

    def test_workflow(self):
        with testfixtures.LogCapture():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                app = BDSSApplication(
                    False, fixtures.get("test_empty.json")
                )
                app._load_workflow()

        self.assertIsInstance(app.workflow_file.workflow, Workflow)

        with testfixtures.LogCapture():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                app = BDSSApplication(
                    True, fixtures.get("test_empty.json")
                )
                app._load_workflow()

        self.assertIsInstance(app.workflow_file.workflow, Workflow)

    def test_nonexistent_file(self):

        # Provide a workflow file path that does not exists
        with testfixtures.LogCapture() as capture:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                app = BDSSApplication(
                    False, fixtures.get("test_nonexistent.json")
                )
                capture.clear()
                with self.assertRaises(FileNotFoundError):
                    app._load_workflow()
            capture.check(
                ('force_bdss.app.bdss_application',
                 'ERROR',
                 "Unable to open workflow file '{}'.".format(
                     fixtures.get("test_nonexistent.json")))
            )
