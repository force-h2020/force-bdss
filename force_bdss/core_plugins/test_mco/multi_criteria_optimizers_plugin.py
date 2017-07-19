from force_bdss.base_extension_plugin import BaseExtensionPlugin

from .dakota.dakota_bundle import DakotaBundle


class MultiCriteriaOptimizersPlugin(BaseExtensionPlugin):
    def _mco_bundles_default(self):
        return [DakotaBundle()]
