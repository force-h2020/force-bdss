
from traits.api import (
    HasStrictTraits,
    provides
)
from force_bdss.mco.optimizers.i_optimizer import (
    IOptimizer
)

from force_bdss.mco.parameters.mco_parameters import (
    FixedMCOParameter,
    RangedMCOParameter,
    ListedMCOParameter,
    CategoricalMCOParameter
)


@provides(IOptimizer)
class ProbeIOptimizer(HasStrictTraits):

    def optimize_function(self, func, params):

        point = []
        for p in params:
            if isinstance(p, FixedMCOParameter):
                point.append(p.value)
            elif isinstance(p, RangedMCOParameter):
                point.append(p.initial_value)
            elif isinstance(p, ListedMCOParameter):
                point.append(p.levels[0])
            elif isinstance(p, CategoricalMCOParameter):
                point.append(p.categories[0])

        # pretend we have 10 points in the Pareto-set
        for _ in range(10):
            yield point
