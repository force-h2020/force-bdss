# Enthought library imports.
from envisage.api import Application


# Application entry point.
from force_bdss.multi_criteria_optimizers_plugin import \
    MultiCriteriaOptimizersPlugin
from force_bdss.workflow_plugin import WorkflowPlugin
from force_bdss.key_performance_calculators_plugin import \
    KeyPerformanceCalculatorsPlugin


def run():

    application = Application(
        id='force',
        plugins=[
            WorkflowPlugin(),
            MultiCriteriaOptimizersPlugin(),
            KeyPerformanceCalculatorsPlugin(),
        ]
    )

    # Run it!
    application.run()
