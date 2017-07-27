import csv
import numpy
from force_bdss.api import BaseDataSource
from force_bdss.api import DataSourceResult


class CSVExtractorDataSource(BaseDataSource):
    def run(self, model, parameters):
        with open(model.filename) as csvfile:
            reader = csv.reader(csvfile)
            for rowindex, row in enumerate(reader):
                if rowindex < model.row:
                    continue

                if rowindex == model.row:
                    return DataSourceResult(
                        originator=self,
                        value_types=[model.cuba_type],
                        values=numpy.array(
                            parameters.values[0]+float(
                                row[model.column])).reshape(1, 1)
                    )

                return None
            return None
