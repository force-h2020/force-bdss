#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import unittest

from traits.trait_errors import TraitError

from force_bdss.ui_hooks.base_ui_hooks_factory import BaseUIHooksFactory
from force_bdss.ui_hooks.tests.test_base_ui_hooks_manager import \
    DummyUIHooksManager


class DummyUIHooksFactory(BaseUIHooksFactory):
    def get_identifier(self):
        return "foo"

    def get_name(self):
        return "bar"

    def get_ui_hooks_manager_class(self):
        return DummyUIHooksManager


class TestBaseUIHooksFactory(unittest.TestCase):
    def setUp(self):
        self.plugin = {'id': "pid", 'name': 'Plugin'}

    def test_initialize(self):
        factory = DummyUIHooksFactory(plugin=self.plugin)
        self.assertEqual(factory.plugin_id, "pid")
        self.assertEqual(factory.plugin_name, 'Plugin')
        self.assertEqual(factory.id, "pid.factory.foo")
        self.assertEqual(factory.name, "bar")
        self.assertEqual(factory.ui_hooks_manager_class, DummyUIHooksManager)
        self.assertIsInstance(factory.create_ui_hooks_manager(),
                              DummyUIHooksManager)

    def test_broken_get_identifier(self):
        class Broken(DummyUIHooksFactory):
            def get_identifier(self):
                return None

        with self.assertRaises(ValueError):
            Broken(self.plugin)

    def test_broken_get_name(self):
        class Broken(DummyUIHooksFactory):
            def get_name(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.plugin)

    def test_broken_get_ui_hooks_manager_class(self):
        class Broken(DummyUIHooksFactory):
            def get_ui_hooks_manager_class(self):
                return None

        with self.assertRaises(TraitError):
            Broken(self.plugin)
