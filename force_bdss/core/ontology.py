import numpy as np

from osp.core import cuba, force_ontology
from osp.core.ontology.namespace import OntologyNamespace
from osp.core.ontology.validator import entity_name_regex

from traits.api import (
    TraitType,
    HasStrictTraits,
    String,
    List,
    Bool,
    Float,
    Int,
    Str,
    Array,
    Any,
    provides
)

from force_bdss.core.i_ontology import IOntology

ONTOLOGY_DATATYPE_CONVERSIONS = {
    'BOOL': {'basic': bool, 'trait': Bool},
    "INT": {'basic': int, 'trait': Int},
    "FLOAT": {'basic': float, 'trait': Float},
    "STRING": {'basic': str, 'trait': Str},
    "UUID": {'basic': str, 'trait': Str},
    "UNDEFINED": {'basic': None, 'trait': Any},
    "VECTOR": {'basic': np.ndarray, 'trait': Array}
}


#: Identifies a CUBA type with its key.
CUBAType = String(regex=entity_name_regex)


class Ontology(TraitType):

    #: The default value for the trait:
    default_value = cuba

    #: A description of the type of value this trait accepts:
    info_text = "an OSP-Core OntologyNamespace object"

    def validate(self, object, name, value):
        """ Validates that a specified value is valid for this trait.

            Note: The 'fast validator' version performs this check in C.
        """
        if isinstance(value, OntologyNamespace):
            return value

        self.error(object, name, value)


@provides(IOntology)
class BDSSOntology(HasStrictTraits):

    #: List of OntologyNamespace objects
    ontologies = List(Ontology, transient=True, visible=False)

    def _ontologies_default(self):
        """Load in the FORCE ontology for basic physical data types"""
        return [force_ontology]

    def cuba_attr(self, cuba_type):
        """Search in loaded ontologies for first OntologyAttribute object
        corresponding to CUBA type string

        Parameters
        ----------
        cuba_type: CUBAType
            Name of attribute to look up
        """
        for ontology in self.ontologies:
            try:
                return getattr(ontology, cuba_type.upper())
            except AttributeError:
                pass

    def cuba_to_basic(self, cuba_type):
        """Return the basic python data type for an
        OntologyAttribute object corresponding to CUBA type
        string

        Parameters
        ----------
        cuba_type: CUBAType
            Name of attribute to look up
        """
        cuba_attr = self.cuba_attr(cuba_type)
        return ONTOLOGY_DATATYPE_CONVERSIONS[cuba_attr.datatype]['basic']

    def cuba_to_trait(self, cuba_type):
        """Return the TraitType for an OntologyAttribute object
        corresponding to CUBA type string

        Parameters
        ----------
        cuba_type: CUBAType
           Name of attribute to look up
        """
        cuba_attr = self.cuba_attr(cuba_type)
        return ONTOLOGY_DATATYPE_CONVERSIONS[cuba_attr.datatype]['trait']
