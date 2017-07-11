import click
from envisage.core_plugin import CorePlugin
import logging

from force_bdss.bdss_application import BDSSApplication
from force_bdss.core_mco_driver import CoreMCODriver
from force_bdss.multi_criteria_optimizers_plugin import \
    MultiCriteriaOptimizersPlugin
from force_bdss.key_performance_calculators_plugin import \
    KeyPerformanceCalculatorsPlugin


@click.command()
@click.option("--evaluate", is_flag=True)
@click.argument('workflow_filepath', type=click.Path(exists=True))
def run(evaluate, workflow_filepath):

    plugins = [
        CorePlugin(),
        CoreMCODriver(),
        KeyPerformanceCalculatorsPlugin(),
        MultiCriteriaOptimizersPlugin(),
    ]

    application = BDSSApplication(
        plugins=plugins,
        evaluate=evaluate,
        workflow_filepath=workflow_filepath
    )

    application.run()
