from osp.core import force_ontology
from numpy import ndarray

from traits.api import (
    provides,
    HasStrictTraits,
    Bool,
    Float,
    Int,
    Str,
    Array,
    Any,
    List
)

from force_bdss.core.i_ontology_registry import IOntologyRegistry
from force_bdss.core.ontology import Ontology


# Note: this is a work around to obtain the python basic and TraitType
# from a CUBA key. The type conversions are only expect to be stable for
# the BDSS deployment environment. It is also expected that future
# versions of osp-core will implement an equivalent method.

# Please also note the behavioural differences between basic python
# and TraitType conversions for the "UNDEFINED" CUBAType. This allows
# for more traits flexibility if the CUBAType is not present in a
# given Ontology object
ONTOLOGY_DATATYPE_CONVERSIONS = {
    'BOOL': {'basic': bool, 'trait': Bool},
    "INT": {'basic': int, 'trait': Int},
    "FLOAT": {'basic': float, 'trait': Float},
    "STRING": {'basic': str, 'trait': Str},
    "UUID": {'basic': str, 'trait': Str},
    "UNDEFINED": {'basic': None, 'trait': Any},
    "VECTOR": {'basic': ndarray, 'trait': Array}
}


@provides(IOntologyRegistry)
class OntologyRegistry(HasStrictTraits):

    #: List of OntologyNamespace objects
    ontologies = List(Ontology, transient=True, visible=False)

    def _ontologies_default(self):
        """Load in the FORCE ontology for basic physical data types"""
        return [force_ontology]

    def cuba_attr(self, cuba_type):
        """Search in loaded ontologies for first OntologyAttribute object
        corresponding to CUBA type string.

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

        # If CUBAType does not exist in any ontology, consider it
        # as a generic OntologyAttribute object with undefined data
        # value attribute
        return getattr(force_ontology, 'VALUE')

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
