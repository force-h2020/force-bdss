from traits.api import Interface, String, Instance


class IMultiCriteriaOptimizer(Interface):
    name = String()

    def run(self, application):
        pass
