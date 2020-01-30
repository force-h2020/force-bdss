from unittest import TestCase

from osp.core.ontology.namespace import OntologyNamespace
from osp.core.ontology.attribute import OntologyAttribute

from traits.api import HasTraits, TraitError

from force_bdss.core.ontology import CUBAType, Ontology, BDSSOntology


class ProbeHasTraits(HasTraits):
    ontology = Ontology()
    cuba = CUBAType()


class TestOntology(TestCase):

    def setUp(self):

        self.probe_class = ProbeHasTraits(
            cuba="VOLUME"
        )
        self.bdss_ontology = BDSSOntology()

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

        for not_allowed in ["0", None, 123, "0hello", "hi$", "hi%"]:
            with self.assertRaises(TraitError):
                self.probe_class.cuba = not_allowed

    def test_bdss_ontology(self):

        self.assertEqual(1, len(self.bdss_ontology.ontologies))
        self.assertIsInstance(
            self.bdss_ontology.ontologies[0], OntologyNamespace)
        self.assertEqual(
            'FORCE_ONTOLOGY', self.bdss_ontology.ontologies[0].name)

        volume = self.bdss_ontology.cuba_attr('Volume')
        self.assertIsInstance(volume, OntologyAttribute)
        self.assertEqual('FLOAT', volume.datatype)

        self.assertEqual(
            float, self.bdss_ontology.python_type('Volume'))
