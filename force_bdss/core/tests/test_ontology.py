from unittest import TestCase

from osp.core.ontology.namespace import OntologyNamespace

from traits.api import HasTraits, TraitError, Float, Any

from force_bdss.core.ontology import (
    CUBAType,
    CUBATypeMixin,
    Ontology
)
from force_bdss.core.ontology_registry import OntologyRegistry


class ProbeHasTraits(HasTraits):
    ontology = Ontology()
    cuba = CUBAType()


class TestOntology(TestCase):

    def setUp(self):

        self.probe_class = ProbeHasTraits(
            cuba="VOLUME"
        )
        self.cuba_type_mixin = CUBATypeMixin()

    def test_ontology_trait_type(self):

        self.assertIsInstance(
            self.probe_class.ontology, OntologyNamespace)
        self.assertEqual(
            'CUBA', self.probe_class.ontology.name)
        self.assertEqual(
            "an OSP-Core OntologyNamespace object",
            Ontology().info())

    def test_cuba_type(self):

        self.assertEqual(self.probe_class.cuba, "VOLUME")

        for allowed in ["ALLCAPS", "Value", "CamelCase"]:
            self.probe_class.cuba = allowed

        for not_allowed in ["0", None, 123, "hello", "$hi", ""]:
            with self.assertRaises(TraitError):
                self.probe_class.cuba = not_allowed

    def test_cuba_type_mixin(self):

        ontology_registry = OntologyRegistry()

        self.assertEqual(
            Any,
            self.cuba_type_mixin.trait_type(ontology_registry))

        self.cuba_type_mixin.type = 'Volume'
        self.assertEqual(
            Float,
            self.cuba_type_mixin.trait_type(ontology_registry))
