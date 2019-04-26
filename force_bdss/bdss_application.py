import functools
import logging

from stevedore.extension import ExtensionManager
from stevedore.exception import NoMatches

from envisage.api import Application
from envisage.core_plugin import CorePlugin
from traits.api import Unicode, Bool, Property
from traits.etsconfig.api import ETSConfig

from force_bdss.ids import InternalPluginID
from .factory_registry_plugin import FactoryRegistryPlugin
from .core_evaluation_driver import CoreEvaluationDriver
from .core_mco_driver import CoreMCODriver

log = logging.getLogger(__name__)


class BDSSApplication(Application):
    """Main application for the BDSS.
    """
    id = "force.bdss_core.bdss_application"

    #: The path of the workflow file to open
    workflow_filepath = Unicode()

    #: This flags signals to the application not to execute and orchestrate
    #: the MCO, but instead to perform a single evaluation under the
    #: coordination of the MCO itself. See design notes for more details.
    evaluate = Bool()

    #: Gives the currently opened workflow
    workflow = Property()

    def __init__(self, evaluate, workflow_filepath):
        # This is a command-line app, we don't want GUI event loops
        try:
            ETSConfig.toolkit = 'null'
        except ValueError:
            # already been set, so can't do anything much
            if ETSConfig.toolkit != 'null':
                log.info(
                    "ETS toolkit is set to '%s', should not override.",
                    ETSConfig.toolkit
                )

        self.evaluate = evaluate
        self.workflow_filepath = workflow_filepath

        plugins = [CorePlugin(), FactoryRegistryPlugin()]

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
            log.info("No extensions found")

        super(BDSSApplication, self).__init__(plugins=plugins)

    def _get_workflow(self):
        if self.evaluate:
            plugin = self.get_plugin(
                InternalPluginID.CORE_EVALUATION_DRIVER_ID)
        else:
            plugin = self.get_plugin(InternalPluginID.CORE_MCO_DRIVER_ID)

        return plugin.workflow


def _import_extensions(plugins, ext):
    """Service routine extracted for testing.
    Imports the extension in the plugins argument.
    """
    log.info("Found extension {}".format(ext.obj))
    plugins.append(ext.obj)


def _load_failure_callback(plugins, manager, entry_point, exception):
    """Service routine extracted for testing.
    Reports failure to load a module through stevedore, using the
    on_load_failure_callback option.
    """
    log.error(
        "Unable to load plugin {}. Exception: {}. Message: {}".format(
            entry_point, exception.__class__.__name__, exception),
        exc_info=True,
    )
