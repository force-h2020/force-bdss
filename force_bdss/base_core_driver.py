from envisage.plugin import Plugin
from traits.trait_types import Instance

from force_bdss.bundle_registry import (
    BundleRegistryPlugin,
    BUNDLE_REGISTRY_PLUGIN_ID
)


class BaseCoreDriver(Plugin):
    """Main plugin that handles the execution of the MCO
    or the evaluation.
    """

    bundle_registry = Instance(BundleRegistryPlugin)

    def _bundle_registry_default(self):
        return self.application.get_plugin(BUNDLE_REGISTRY_PLUGIN_ID)
