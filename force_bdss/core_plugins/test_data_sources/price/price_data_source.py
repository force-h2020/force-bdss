from force_bdss.data_sources.base_data_source import BaseDataSource


class PriceDataSource(BaseDataSource):
    def run(self):
        print("Computing price")
