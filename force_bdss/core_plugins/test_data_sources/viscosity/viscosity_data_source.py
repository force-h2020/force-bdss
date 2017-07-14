from force_bdss.data_sources.base_data_source import BaseDataSource


class ViscosityDataSource(BaseDataSource):
    def run(self):
        print("Computing viscosity")
