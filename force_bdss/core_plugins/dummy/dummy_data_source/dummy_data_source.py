from force_bdss.api import BaseDataSource, DataSourceResult


class DummyDataSource(BaseDataSource):
    def run(self, parameters):
        print(parameters)
        return DataSourceResult(
                originator=self,
                value_names=parameters.value_names,
                value_types=parameters.value_types,
                values=parameters.values.reshape(
                    parameters.values.shape + (1,)))
