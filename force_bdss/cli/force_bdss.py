import logging
import click

from ..bdss_application import BDSSApplication

# Makes the application rethrow the exception so that it exits return code
# different from zero.
from traits.api import push_exception_handler
push_exception_handler(reraise_exceptions=True)


@click.command()
@click.option("--evaluate",
              is_flag=True,
              help="Runs the evaluation for a single point.")
@click.option("--run-data-source",
              type=click.STRING,
              help="If specified, runs only the specified datasource "
                   "interactively. This is useful for debugging.")
@click.option("--logfile",
              type=click.Path(exists=False),
              help="If specified, the log filename. "
                   " If unspecified, the log will be written to stdout.")
@click.argument('workflow_filepath', type=click.Path(exists=True))
def run(evaluate, run_data_source, logfile, workflow_filepath):

    logging_config = {}
    logging_config["level"] = logging.INFO

    if logfile is not None:
        logging_config["filename"] = logfile

    logging.basicConfig(**logging_config)
    log = logging.getLogger(__name__)

    try:
        application = BDSSApplication(
            evaluate=evaluate,
            run_data_source=run_data_source,
            workflow_filepath=workflow_filepath
        )

        application.run()
    except Exception as e:
        log.exception(e)

