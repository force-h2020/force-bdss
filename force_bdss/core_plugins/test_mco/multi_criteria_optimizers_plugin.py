from force_bdss.api import BaseExtensionPlugin

from .dakota.dakota_bundle import DakotaBundle


class MultiCriteriaOptimizersPlugin(BaseExtensionPlugin):
    def _mco_bundles_default(self):
        return [DakotaBundle()]
