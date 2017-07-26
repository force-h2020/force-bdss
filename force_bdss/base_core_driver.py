from envisage.plugin import Plugin
from traits.trait_types import Instance

from .bundle_registry_plugin import (
    BundleRegistryPlugin,
    BUNDLE_REGISTRY_PLUGIN_ID
)
from .io.workflow_reader import WorkflowReader
from .workspecs.workflow import Workflow
from .mco.parameters.mco_parameter_factory_registry import (
    MCOParameterFactoryRegistry)
from .mco.parameters.core_mco_parameters import all_core_factories


class BaseCoreDriver(Plugin):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    #: The registry of the bundles.
    bundle_registry = Instance(BundleRegistryPlugin)

    #: The registry of the MCO parameters
    parameter_factory_registry = Instance(MCOParameterFactoryRegistry)

    #: Deserialized content of the workflow file.
    workflow = Instance(Workflow)

    def _bundle_registry_default(self):
        return self.application.get_plugin(BUNDLE_REGISTRY_PLUGIN_ID)

    def _parameter_factory_registry_default(self):
        registry = MCOParameterFactoryRegistry()
        for f in all_core_factories():
            registry.register(f)

        return registry

    def _workflow_default(self):
        reader = WorkflowReader(self.bundle_registry,
                                self.parameter_factory_registry)
        with open(self.application.workflow_filepath) as f:
            return reader.read(f)
