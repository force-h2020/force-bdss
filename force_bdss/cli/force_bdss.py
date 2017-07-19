import click

from ..bdss_application import BDSSApplication
from traits.api import push_exception_handler
push_exception_handler(reraise_exceptions=True)

@click.command()
@click.option("--evaluate", is_flag=True)
@click.argument('workflow_filepath', type=click.Path(exists=True))
def run(evaluate, workflow_filepath):

    application = BDSSApplication(
        evaluate=evaluate,
        workflow_filepath=workflow_filepath
    )

    application.run()
