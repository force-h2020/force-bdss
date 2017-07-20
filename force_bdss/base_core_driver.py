from envisage.plugin import Plugin
from traits.trait_types import Instance

from .bundle_registry_plugin import (
    BundleRegistryPlugin,
    BUNDLE_REGISTRY_PLUGIN_ID
)
from .io.workflow_reader import WorkflowReader
from .workspecs.workflow import Workflow


class BaseCoreDriver(Plugin):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    bundle_registry = Instance(BundleRegistryPlugin)

    #: Deserialized content of the workflow file.
    workflow = Instance(Workflow)

    def _bundle_registry_default(self):
        return self.application.get_plugin(BUNDLE_REGISTRY_PLUGIN_ID)

    def _workflow_default(self):
        reader = WorkflowReader(self.bundle_registry)
        with open(self.application.workflow_filepath) as f:
            return reader.read(f)
