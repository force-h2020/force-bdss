import csv
import numpy
from force_bdss.data_sources.base_data_source import BaseDataSource
from force_bdss.data_sources.data_source_result import DataSourceResult


class CSVExtractorDataSource(BaseDataSource):
    def run(self, parameters):
        with open(self.model.filename) as csvfile:
            reader = csv.reader(csvfile)
            for rowindex, row in enumerate(reader):
                if rowindex < self.model.row:
                    continue

                if rowindex == self.model.row:
                    return DataSourceResult(
                        originator=self,
                        value_types=[self.model.cuba_type],
                        values=numpy.array(
                            parameters.values[0]+float(
                                row[self.model.column])).reshape(1, 1)
                    )

                return None
            return None
