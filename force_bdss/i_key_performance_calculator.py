from traits.api import Interface


class IKeyPerformanceCalculator(Interface):
    def run(self):
        pass
