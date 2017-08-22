import unittest

from ..base_ui_hooks_factory import BaseUIHooksFactory
try:
    import mock
except ImportError:
    from unittest import mock


class TestBaseUIHooksFactory(unittest.TestCase):

