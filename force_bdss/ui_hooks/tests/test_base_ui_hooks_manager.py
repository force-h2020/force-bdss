#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from force_bdss.tests.dummy_classes.ui_hooks import DummyUIHooksManager
from force_bdss.ui_hooks.base_ui_hooks_factory import BaseUIHooksFactory

from unittest import mock


class TestBaseUIHooksManager(unittest.TestCase):
    def test_initialization(self):
        mock_factory = mock.Mock(spec=BaseUIHooksFactory)
        mgr = DummyUIHooksManager(mock_factory)

        self.assertEqual(mgr.factory, mock_factory)
