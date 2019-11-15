import testfixtures
from unittest import TestCase

from traits.api import HasTraits, Int, Unicode

from force_bdss.data_sources.data_source_utilities import (
    have_similar_attribute, different_attributes, merge_trait_with_check,
    merge_trait, TraitSimilarityError
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

    def test_merge_trait(self):

        merge_trait(self.new_trait, self.old_trait, 'a_string')

        self.assertEqual('new', self.old_trait.a_string)

        self.old_trait = DummyTrait()
        self.new_trait = DummyTrait(an_integer=10, a_string='new')
        merge_trait(self.old_trait, self.new_trait, 'a_string')

        self.assertEqual('new', self.old_trait.a_string)

    def test_trait_similarity_check(self):

        self.assertFalse(
            have_similar_attribute(
                self.old_trait, self.new_trait, 'an_integer'
            )
        )
        self.assertTrue(
            have_similar_attribute(
                self.old_trait, self.new_trait, 'an_integer',
                ignore_default=True
            )
        )

        self.assertFalse(
            have_similar_attribute(
                self.new_trait, self.old_trait, 'a_string'
            )
        )
        self.assertTrue(
            have_similar_attribute(
                self.new_trait, self.old_trait, 'a_string',
                ignore_default=True
            )
        )

        self.assertTrue(
            have_similar_attribute(
                self.old_trait, self.new_trait, '__class__'
            )
        )
        self.assertTrue(
            have_similar_attribute(
                self.old_trait, self.new_trait, '__class__',
                ignore_default=True
            )
        )

        another_trait = AnotherDummyTrait()
        self.assertTrue(
            have_similar_attribute(
                self.old_trait, another_trait, 'an_integer',
                ignore_default=True)
        )

    def test_attr_checker(self):
        failed_attr = different_attributes(
            self.old_trait, self.new_trait,
            '__class__',
        )
        self.assertEqual(0, len(failed_attr))

        failed_attr = different_attributes(
            self.old_trait, self.new_trait,
            '__class__', ignore_default=True
        )
        self.assertEqual(0, len(failed_attr))

        failed_attr = different_attributes(
            self.old_trait, self.new_trait,
            ['__class__', 'an_integer', 'a_string']
        )
        self.assertEqual(2, len(failed_attr))
        self.assertListEqual(['an_integer', 'a_string'], failed_attr)

        failed_attr = different_attributes(
            self.old_trait, self.new_trait,
            ['__class__', 'an_integer', 'a_string'],
            ignore_default=True
        )
        self.assertEqual(0, len(failed_attr))

        with self.assertRaises(AttributeError):
            different_attributes(
                self.old_trait, self.new_trait,
                ['not_an_attr']
            )

    def test_merge_trait_with_check(self):

        merge_trait_with_check(
            self.new_trait, self.old_trait, 'an_integer'
        )
        self.assertEqual(10, self.old_trait.an_integer)
        merge_trait_with_check(
            self.old_trait, self.new_trait, 'an_integer'
        )
        self.assertEqual(10, self.old_trait.an_integer)

        merge_trait_with_check(
            self.new_trait, self.old_trait,
            attributes=['a_string', 'an_integer']
        )
        self.assertEqual('new', self.old_trait.a_string)
        merge_trait_with_check(
            self.new_trait, self.old_trait,
            attributes='a_string'
        )
        self.assertEqual('new', self.old_trait.a_string)

        another_trait = AnotherDummyTrait(a_string='new')
        with testfixtures.LogCapture():
            with self.assertRaises(TraitSimilarityError):
                merge_trait_with_check(
                    another_trait, self.old_trait,
                    attributes=['a_string', 'an_integer'],
                    ignore_default=False
                )

        merge_trait_with_check(
            another_trait, self.old_trait,
            attributes=['a_string', 'an_integer'],
            ignore_default=True)
        self.assertEqual('new', self.old_trait.a_string)
