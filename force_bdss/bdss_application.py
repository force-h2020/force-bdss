import json

from stevedore import extension
from stevedore.exception import NoMatches
from envisage.api import Application
from envisage.core_plugin import CorePlugin

from force_bdss.bundle_registry import BundleRegistryPlugin
from force_bdss.core_evaluation_driver import CoreEvaluationDriver
from force_bdss.core_mco_driver import CoreMCODriver

from traits.api import Unicode, Bool, Instance

from force_bdss.workspecs.workflow import Workflow


class BDSSApplication(Application):
    """Main application for the BDSS.
    """
    id = "force_bdss.bdss_application"

    #: The path of the workflow file to open
    workflow_filepath = Unicode()

    #: Deserialized content of the workflow file.
    workflow = Instance(Workflow)

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

    def _workflow_default(self):
        with open(self.workflow_filepath) as f:
            return Workflow.from_json(json.load(f))
