from unittest import TestCase

from osp.core.ontology.namespace import OntologyNamespace
from osp.core.ontology.attribute import OntologyAttribute

from traits.api import Float, Any

from force_bdss.core.ontology_registry import OntologyRegistry


class TestOntologyRegistry(TestCase):

    def setUp(self):
        self.ontology_registry = OntologyRegistry()

    def test_ontology_registry(self):

        self.assertEqual(1, len(self.ontology_registry.ontologies))
        self.assertIsInstance(
            self.ontology_registry.ontologies[0], OntologyNamespace)
        self.assertEqual(
            'FORCE_ONTOLOGY', self.ontology_registry.ontologies[0].name)

        volume = self.ontology_registry.cuba_attr('Volume')
        self.assertIsInstance(volume, OntologyAttribute)
        self.assertEqual('FLOAT', volume.datatype)
        self.assertEqual(
            float, self.ontology_registry.cuba_to_basic('Volume'))
        self.assertEqual(
            Float, self.ontology_registry.cuba_to_trait('Volume'))

        # Handling of CUBA type not in any ontology
        not_present = self.ontology_registry.cuba_attr('NotPresent')
        self.assertIsInstance(not_present, OntologyAttribute)
        self.assertEqual('UNDEFINED', not_present.datatype)
        self.assertEqual(
            None, self.ontology_registry.cuba_to_basic('NotPresent'))
        self.assertEqual(
            Any, self.ontology_registry.cuba_to_trait('NotPresent'))
