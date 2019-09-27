from unittest import TestCase

from traits.api import HasTraits, Int, Unicode

from force_bdss.data_sources.utilities import (
    trait_check, attr_checker, sync_trait_with_check
)


class DummyTrait(HasTraits):

    an_integer = Int(5)

    a_string = Unicode('default')


class AnotherDummyTrait(HasTraits):

    an_integer = Int(20)

    a_string = Unicode('default')


class TestUtilities(TestCase):

    def setUp(self):
        self.old_trait = DummyTrait()
        self.new_trait = DummyTrait(an_integer=10, a_string='new')

    def test_trait_check(self):

        self.assertFalse(
            trait_check(self.old_trait, self.new_trait, 'an_integer')
        )
        self.assertTrue(
            trait_check(self.old_trait, self.new_trait, '__class__')
        )
        self.assertTrue(
            trait_check(self.old_trait, self.new_trait, '__class__',
                        ignore_default=True)
        )

        another_trait = AnotherDummyTrait()
        self.assertTrue(
            trait_check(self.old_trait, another_trait, 'an_integer',
                        ignore_default=True)
        )

    def test_attr_checker(self):
        failed_attr = attr_checker(
            self.old_trait, self.new_trait,
            '__class__',
        )
        self.assertEqual(0, len(failed_attr))

        failed_attr = attr_checker(
            self.old_trait, self.new_trait,
            ['__class__', 'an_integer', 'a_string']
        )

        self.assertEqual(2, len(failed_attr))
        self.assertListEqual(['an_integer', 'a_string'], failed_attr)

        with self.assertRaises(AttributeError):
            attr_checker(
                self.old_trait, self.new_trait,
                ['not_an_attr']
            )

    def test_sync_trait_with_check(self):
        sync_trait_with_check(self.new_trait, self.old_trait,
                              'an_integer')
        self.assertEqual(10, self.old_trait.an_integer)

        sync_trait_with_check(self.new_trait, self.old_trait,
                              'a_string', attr_checks=['an_integer'])
        self.assertEqual('new', self.old_trait.a_string)

        sync_trait_with_check(self.new_trait, self.old_trait,
                              'a_string', attr_checks='an_integer')
        self.assertEqual('new', self.old_trait.a_string)

        another_trait = AnotherDummyTrait(a_string='new')
        with self.assertRaises(RuntimeError):
            sync_trait_with_check(another_trait, self.old_trait,
                                  'a_string', attr_checks=['an_integer'])

        with self.assertRaises(RuntimeError):
            sync_trait_with_check(another_trait, self.old_trait,
                                  'a_string', attr_checks='__class__')

        sync_trait_with_check(
            another_trait, self.old_trait, 'a_string',
            attr_checks=['an_integer'], ignore_default=True)
        self.assertEqual('new', self.old_trait.a_string)
