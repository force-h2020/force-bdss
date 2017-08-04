from envisage.plugin import Plugin
from traits.trait_types import Instance

from .core.workflow import Workflow
from .factory_registry_plugin import (
    FactoryRegistryPlugin,
    FACTORY_REGISTRY_PLUGIN_ID
)
from .io.workflow_reader import WorkflowReader


class BaseCoreDriver(Plugin):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    #: The registry of the factories
    factory_registry = Instance(FactoryRegistryPlugin)

    #: Deserialized content of the workflow file.
    workflow = Instance(Workflow)

    def _factory_registry_default(self):
        return self.application.get_plugin(FACTORY_REGISTRY_PLUGIN_ID)

    def _workflow_default(self):
        reader = WorkflowReader(self.factory_registry)
        with open(self.application.workflow_filepath) as f:
            return reader.read(f)
