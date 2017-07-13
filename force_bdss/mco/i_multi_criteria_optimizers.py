from traits.api import Interface, String


class IMultiCriteriaOptimizer(Interface):
    name = String()

    def run(self, application):
        pass
