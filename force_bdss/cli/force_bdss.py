import click

from force_bdss.bdss_application import BDSSApplication


@click.command()
@click.option("--evaluate", is_flag=True)
@click.argument('workflow_filepath', type=click.Path(exists=True))
def run(evaluate, workflow_filepath):

    application = BDSSApplication(
        evaluate=evaluate,
        workflow_filepath=workflow_filepath
    )

    application.run()
