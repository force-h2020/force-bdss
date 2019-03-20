from traits.api import Enum, HasStrictTraits

from force_bdss.io.workflow_writer import pop_dunder_recursive
from force_bdss.local_traits import Identifier


class KPISpecification(HasStrictTraits):
    #: The user defined name of the variable containing the kpi value.
    name = Identifier()

    #: The expected outcome of the procedure relative to this KPI.
    objective = Enum("MINIMISE", "MAXIMISE")

    def __getstate__(self):
        return pop_dunder_recursive(super().__getstate__())
