import functools
import logging

from stevedore.extension import ExtensionManager
from stevedore.exception import NoMatches

from envisage.api import Application
from envisage.core_plugin import CorePlugin
from traits.api import Unicode, Bool

from .bundle_registry_plugin import BundleRegistryPlugin
from .core_evaluation_driver import CoreEvaluationDriver
from .core_mco_driver import CoreMCODriver


class BDSSApplication(Application):
    """Main application for the BDSS.
    """
    id = "force_bdss.bdss_application"

    #: The path of the workflow file to open
    workflow_filepath = Unicode()

    #: This flags signals to the application not to execute and orchestrate
    #: the MCO, but instead to perform a single evaluation under the
    #: coordination of the MCO itself. See design notes for more details.
    evaluate = Bool()

    def __init__(self, evaluate, workflow_filepath):
        self.evaluate = evaluate
        self.workflow_filepath = workflow_filepath

        plugins = [CorePlugin(), BundleRegistryPlugin()]

        if self.evaluate:
            plugins.append(CoreEvaluationDriver())
        else:
            plugins.append(CoreMCODriver())

        mgr = ExtensionManager(
            namespace='force.bdss.extensions',
            invoke_on_load=True,
            on_load_failure_callback=functools.partial(_load_failure_callback,
                                                       plugins)
        )

        try:
            mgr.map(functools.partial(_import_extensions, plugins))
        except NoMatches:
            logging.info("No extensions found")

        super(BDSSApplication, self).__init__(plugins=plugins)


def _import_extensions(plugins, ext):
    """Service routine extracted for testing.
    Imports the extension in the plugins argument.
    """
    logging.info("Found extension {}".format(ext.obj))
    plugins.append(ext.obj)


def _load_failure_callback(plugins, manager, entry_point, exception):
    """Service routine extracted for testing.
    Reports failure to load a module through stevedore, using the
    on_load_failure_callback option.
    """
    logging.error(
        "Unable to load plugin {}. Exception: {}. Message: {}".format(
            entry_point, exception.__class__.__name__, exception)
    )
