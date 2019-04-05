import logging
import click

from traits.api import push_exception_handler

from traits.etsconfig.api import ETSConfig

# This is a CLI app, so ETS toolkit should be null
ETSConfig.toolkit = 'null'

# Makes the application rethrow the exception so that it exits return code
# different from zero.
push_exception_handler(reraise_exceptions=True)


@click.command()
@click.option("--evaluate", is_flag=True)
@click.option("--logfile",
              type=click.Path(exists=False),
              help="If specified, the log filename. "
                   " If unspecified, the log will be written to stdout.")
@click.argument('workflow_filepath', type=click.Path(exists=True))
def run(evaluate, logfile, workflow_filepath):
    from ..bdss_application import BDSSApplication

    logging_config = {}
    logging_config["level"] = logging.INFO

    if logfile is not None:
        logging_config["filename"] = logfile

    logging.basicConfig(**logging_config)
    log = logging.getLogger(__name__)

    try:
        application = BDSSApplication(
            evaluate=evaluate,
            workflow_filepath=workflow_filepath
        )

        application.run()
    except Exception as e:
        log.exception(e)
