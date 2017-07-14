import csv
from force_bdss.data_sources.base_data_source import BaseDataSource


class CSVExtractorDataSource(BaseDataSource):
    def run(self):
        with open(self.model.filename) as csvfile:
            reader = csv.reader(csvfile)
            for rowindex, row in enumerate(reader):
                if rowindex < self.model.row:
                    continue

                if rowindex == self.model.row:
                    return {
                        self.model.cuba_type: row[self.model.column]
                    }

                return None
            return None
