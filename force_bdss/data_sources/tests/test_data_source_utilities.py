import testfixtures
from unittest import TestCase

from traits.api import HasTraits, Int, Unicode

from force_bdss.data_sources.data_source_utilities import (
    have_similar_attribute, different_attributes, check_attributes_are_similar,
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

    def test_check_attributes_are_similar(self):

        another_trait = AnotherDummyTrait(an_integer=5)

        # Test successful checking single attribute
        check_attributes_are_similar(
            another_trait, self.old_trait, 'an_integer'
        )

        # Test unsuccessful checking single attribute
        with testfixtures.LogCapture() as capture:
            with self.assertRaises(TraitSimilarityError):
                check_attributes_are_similar(
                    self.new_trait, self.old_trait, 'an_integer'
                )
            capture.check(
                ('force_bdss.data_sources.data_source_utilities',
                 'ERROR',
                 'Source object has failed a trait similarity'
                 ' check with target:\nThe an_integer attribute '
                 "of source (10) doesn't match target (5).")
            )

        # Test checking list of attributes
        check_attributes_are_similar(
            another_trait, self.old_trait,
            attributes=['a_string', 'an_integer']
        )

        # Test checking list whilst ignoring default values
        check_attributes_are_similar(
            another_trait, self.old_trait,
            attributes=['a_string', 'an_integer'],
            ignore_default=True)

        # Test unsuccessful checking list of attributes
        with testfixtures.LogCapture() as capture:
            with self.assertRaises(TraitSimilarityError):
                check_attributes_are_similar(
                    self.new_trait, self.old_trait,
                    attributes=['a_string', 'an_integer'],
                    ignore_default=False
                )
            capture.check(
                ('force_bdss.data_sources.data_source_utilities',
                 'ERROR',
                 'Source object has failed a trait similarity '
                 'check with target:\nThe a_string attribute of '
                 "source (new) doesn't match target (default).\n"
                 "The an_integer attribute of source (10) "
                 "doesn't match target (5).")
            )
