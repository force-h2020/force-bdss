from traits.api import Interface, String


class IDataSource(Interface):
    computes = String()

    def run(self):
        pass
