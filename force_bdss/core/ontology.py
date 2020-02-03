from osp.core import cuba
from osp.core.ontology.namespace import OntologyNamespace
from osp.core.ontology.validator import entity_name_regex

from traits.api import TraitType, HasStrictTraits, String


#: Identifies a CUBA type with its key.
CUBAType = String(regex=entity_name_regex)


class CUBATypeMixin(HasStrictTraits):

    #: A CUBA key describing the type of the parameter
    type = CUBAType('Value', visible=False)

    def trait_type(self, ontology_registry):
        """Return the TraitType for an IOntologyRegistry object
        corresponding to CUBA type string

        Parameters
        ----------
        ontology_registry: IOntologyRegistry
           Class that fulfills the IOntologyRegistry interface
        """
        return ontology_registry.cuba_to_trait(self.type)


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
