import click
from envisage.core_plugin import CorePlugin

from force_bdss.bdss_application import BDSSApplication
from force_bdss.core_mco_driver import CoreMCODriver
from force_bdss.data_sources.data_sources_plugin import \
    DataSourcesPlugin
from force_bdss.mco.multi_criteria_optimizers_plugin import \
    MultiCriteriaOptimizersPlugin


@click.command()
@click.option("--evaluate", is_flag=True)
@click.argument('workflow_filepath', type=click.Path(exists=True))
def run(evaluate, workflow_filepath):

    plugins = [
        CorePlugin(),
        CoreMCODriver(),
        DataSourcesPlugin(),
        MultiCriteriaOptimizersPlugin(),
    ]

    application = BDSSApplication(
        plugins=plugins,
        evaluate=evaluate,
        workflow_filepath=workflow_filepath
    )

    application.run()
