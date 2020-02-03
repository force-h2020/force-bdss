from traits.has_traits import Interface


class IOntologyRegistry(Interface):

    def cuba_to_basic(self, cuba_type):
        """Return the basic python data type for an
        OntologyAttribute object corresponding to CUBA type
        string

        Parameters
        ----------
        cuba_type: CUBAType
            Name of attribute to look up
        """

    def cuba_to_trait(self, cuba_type):
        """Return the TraitType for an OntologyAttribute object
        corresponding to CUBA type string

        Parameters
        ----------
        cuba_type: CUBAType
           Name of attribute to look up
        """
