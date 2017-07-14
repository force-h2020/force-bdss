import click
from stevedore import extension
from stevedore.exception import NoMatches
from envisage.core_plugin import CorePlugin

from force_bdss.bdss_application import BDSSApplication
from force_bdss.core_mco_driver import CoreMCODriver


@click.command()
@click.option("--evaluate", is_flag=True)
@click.argument('workflow_filepath', type=click.Path(exists=True))
def run(evaluate, workflow_filepath):

    plugins = [
        CorePlugin(),
        CoreMCODriver(),
    ]

    mgr = extension.ExtensionManager(
        namespace='force.bdss.extensions',
        invoke_on_load=True
    )

    def import_extensions(ext):
        print("Found extension {}".format(ext.name))
        plugins.append(ext.obj)

    try:
        mgr.map(import_extensions)
    except NoMatches:
        print("No extensions found")

    application = BDSSApplication(
        plugins=plugins,
        evaluate=evaluate,
        workflow_filepath=workflow_filepath
    )

    application.run()
