from traits.api import HasStrictTraits, Enum

from ..local_traits import Identifier


class InputSlotMap(HasStrictTraits):
    """
    Class that specifies the origin of data for the slots of a data source.
    This entity will go in the model object, and associates the order
    it is in the containing tlist with the variable name the value
    should be taken from.
    """
    #: Where the value will come from.
    #: At the moment, only MCO is supported: the source is the MCO parameter
    #: with name specified at ``name``.
    source = Enum('MCO')

    #: The user defined name of the variable containing the value.
    name = Identifier()
