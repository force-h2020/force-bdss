from force_bdss.data_sources.base_data_source import BaseDataSource


class BasicDataSource(BaseDataSource):
    def run(self):
        print("Computing basic key performance indicator")
