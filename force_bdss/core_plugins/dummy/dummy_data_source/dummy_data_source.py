from force_bdss.api import BaseDataSource


class DummyDataSource(BaseDataSource):
    def run(self, model, parameters):
        return parameters
