import functools
import logging
import sys

from stevedore.extension import ExtensionManager
from stevedore.exception import NoMatches

from envisage.api import Application
from envisage.core_plugin import CorePlugin
from traits.api import Instance
from traits.etsconfig.api import ETSConfig

from force_bdss.core.i_factory_registry import IFactoryRegistry
from force_bdss.core_plugins.factory_registry_plugin import (
    FactoryRegistryPlugin
)
from force_bdss.io.workflow_reader import WorkflowReader
from .workflow_file import WorkflowFile
from .i_operation import IOperation


log = logging.getLogger(__name__)


class BDSSApplication(Application):
    id = "force.bdss_core.bdss_application"

    #: The factory registry for workflow components.
    factory_registry = Instance(IFactoryRegistry)

    #: The workflow file being used.
    workflow_file = Instance(WorkflowFile, allow_none=False)

    #: The operation to be performed.
    operation = Instance(IOperation)

    def __init__(self, evaluate, workflow_file, toolkit='null', **traits):
        self._set_ets_toolkit(toolkit)

        if isinstance(workflow_file, str):
            workflow_file = WorkflowFile(path=workflow_file)

        operation = self._create_operation(evaluate)
        operation.workflow_file = workflow_file

        plugins = [CorePlugin(), FactoryRegistryPlugin()]
        self._load_plugins(plugins)

        super(BDSSApplication, self).__init__(
            workflow_file=workflow_file,
            operation=operation,
            plugins=plugins,
            **traits
        )

    def run(self):
        if self.start():
            # read the workflow
            self.workflow_file.reader = WorkflowReader(self.factory_registry)
            try:
                self.workflow_file.read()
            except Exception:
                log.exception(
                    "Unable to open workflow file '{}'.".format(
                        self.workflow_file.path
                    )
                )
                self.stop()
                sys.exit(1)

            # Do the actual work.
            try:
                self.operation.run()
            except Exception:
                log.exception("Error running workflow.")
                self.stop()
                sys.exit(1)

            self.stop()

    def _set_ets_toolkit(self, toolkit='null'):
        # This is a command-line app, we don't want GUI event loops
        try:
            ETSConfig.toolkit = toolkit
        except ValueError:
            # already been set, so can't do anything much
            if ETSConfig.toolkit != toolkit:
                log.info(
                    "ETS toolkit is set to '%s', should not override.",
                    ETSConfig.toolkit
                )
            else:
                log.debug("ETS toolkit set to '%s'", toolkit)

    def _create_operation(self, evaluate):
        """ Create the appropriate operation instance. """
        if evaluate:
            from .evaluate_operation import EvaluateOperation
            return EvaluateOperation()
        else:
            from .optimize_operation import OptimizeOperation
            return OptimizeOperation()

    def _load_plugins(self, plugins):
        """ Load plugins via Stevedore. """
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

    def _factory_registry_default(self):
        return self.get_service(IFactoryRegistry)


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
