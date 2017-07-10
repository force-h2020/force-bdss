from traits.api import Interface


class IMultiCriteriaOptimizer(Interface):
    def run(self):
        pass
