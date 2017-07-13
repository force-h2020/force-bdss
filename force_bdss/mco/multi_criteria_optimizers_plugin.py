from envisage.plugin import Plugin
from traits.api import List

from force_bdss.mco.basic import Basic
from force_bdss.mco.dakota import Dakota
from force_bdss.mco.i_multi_criteria_optimizers import IMultiCriteriaOptimizer


class MultiCriteriaOptimizersPlugin(Plugin):
    id = "force_bdss.multi_criteria_optimizers_plugin"

    multi_criteria_optimizers = List(
        IMultiCriteriaOptimizer,
        contributes_to='force_bdss.multi_criteria_optimizers'
    )

    def _multi_criteria_optimizers_default(self):
        return [Basic(), Dakota()]
