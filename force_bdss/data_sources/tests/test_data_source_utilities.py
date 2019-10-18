from unittest import TestCase

from traits.api import HasTraits, Int, Unicode

from force_bdss.data_sources.data_source_utilities import (
    trait_similarity_check, attr_checker, merge_trait_with_check
)


class DummyTrait(HasTraits):

    an_integer = Int(5)

    a_string = Unicode('default')


class AnotherDummyTrait(HasTraits):

    an_integer = Int(20)

    a_string = Unicode('default')


class TestDataSourceUtilities(TestCase):

    def setUp(self):
        self.old_trait = DummyTrait()
        self.new_trait = DummyTrait(an_integer=10, a_string='new')

    def test_trait_similarity_check(self):

        self.assertFalse(
            trait_similarity_check(
                self.old_trait, self.new_trait, 'an_integer')
        )
        self.assertTrue(
            trait_similarity_check(
                self.old_trait, self.new_trait, '__class__')
        )
        self.assertTrue(
            trait_similarity_check(
                self.old_trait, self.new_trait, '__class__',
                ignore_default=True)
        )

        another_trait = AnotherDummyTrait()
        self.assertTrue(
            trait_similarity_check(
                self.old_trait, another_trait, 'an_integer',
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

    def test_merge_trait_with_check(self):
        merge_trait_with_check(
            self.new_trait, self.old_trait, 'an_integer')
        self.assertEqual(10, self.old_trait.an_integer)

        merge_trait_with_check(
            self.new_trait, self.old_trait,
            'a_string', attributes=['an_integer'])
        self.assertEqual('new', self.old_trait.a_string)

        merge_trait_with_check(
            self.new_trait, self.old_trait,
            'a_string', attributes='an_integer')
        self.assertEqual('new', self.old_trait.a_string)

        another_trait = AnotherDummyTrait(a_string='new')
        with self.assertRaises(RuntimeError):
            merge_trait_with_check(
                another_trait, self.old_trait,
                'a_string', attributes=['an_integer'])

        with self.assertRaises(RuntimeError):
            merge_trait_with_check(
                another_trait, self.old_trait,
                'a_string', attributes='__class__')

        merge_trait_with_check(
            another_trait, self.old_trait, 'a_string',
            attributes=['an_integer'], ignore_default=True)
        self.assertEqual('new', self.old_trait.a_string)
