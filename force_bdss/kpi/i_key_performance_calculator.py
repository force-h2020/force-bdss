from traits.api import Interface, String


class IKeyPerformanceCalculator(Interface):
    computes = String()

    def run(self):
        pass
