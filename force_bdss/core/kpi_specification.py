from traits.api import Enum, HasStrictTraits

from force_bdss.local_traits import Identifier


class KPISpecification(HasStrictTraits):
    #: The user defined name of the variable containing the kpi value.
    name = Identifier()

    target = Enum("MINIMISE")
