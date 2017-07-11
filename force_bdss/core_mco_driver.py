from envisage.extension_point import ExtensionPoint
from envisage.plugin import Plugin
from traits.has_traits import on_trait_change
from traits.trait_types import List

from force_bdss.i_key_performance_calculator import IKeyPerformanceCalculator
from force_bdss.i_multi_criteria_optimizers import IMultiCriteriaOptimizer


class CoreMCODriver(Plugin):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    # Note: we are forced to declare these extensions points here instead
    # of the application object, and this is why we have to use this plugin.
    # It is a workaround to an envisage bug that does not find the extension
    # points if declared on the application.

    #: A List of the available Multi Criteria Optimizers.
    #: This will be populated by MCO plugins.
    multi_criteria_optimizers = ExtensionPoint(
        List(IMultiCriteriaOptimizer),
        id='force_bdss.multi_criteria_optimizers')

    #: A list of the available Key Performance Indicator calculators.
    #: It will be populated by plugins.
    key_performance_calculators = ExtensionPoint(
        List(IKeyPerformanceCalculator),
        id='force_bdss.key_performance_calculators')

    @on_trait_change("application:started")
    def application_started(self):
        if self.application.evaluate:
            for kpi in self.key_performance_calculators:
                kpi.run(self.application)
        else:
            for mco in self.multi_criteria_optimizers:
                mco.run(self.application)
