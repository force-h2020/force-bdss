import unittest
import testfixtures

from force_bdss.bdss_application import (
    BDSSApplication,
    _load_failure_callback,
    _import_extensions
)

try:
    import mock
except ImportError:
    from unittest import mock


class TestBDSSApplication(unittest.TestCase):
    def test_initialization(self):
        app = BDSSApplication(False, "foo/bar")
        self.assertFalse(app.evaluate)
        self.assertEqual(app.workflow_filepath, "foo/bar")

    def test_extension_load_failure(self):
        plugins = []
        with testfixtures.LogCapture() as log:
            _load_failure_callback(plugins,
                                   mock.Mock(),
                                   "foo",
                                   Exception("hello"))

        log.check(
            ('root', 'ERROR', "Unable to load plugin foo. Exception: "
                              "Exception. Message: hello")
        )
        self.assertEqual(plugins, [])

    def test_import_extension(self):
        plugins = []
        plugin = mock.Mock()
        ext = mock.Mock()
        ext.obj = plugin
        _import_extensions(plugins, ext)

        self.assertEqual(plugins[0], plugin)

