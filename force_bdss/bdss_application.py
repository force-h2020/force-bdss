from stevedore import extension
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

        super(BDSSApplication, self).__init__(plugins=plugins)
