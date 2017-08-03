import csv
from force_bdss.api import BaseDataSource, DataValue
from force_bdss.core.slot import Slot


class CSVExtractorDataSource(BaseDataSource):
    def run(self, model, parameters):
        with open(model.filename) as csvfile:
            reader = csv.reader(csvfile)
            for rowindex, row in enumerate(reader):
                if rowindex < model.row:
                    continue
                elif rowindex == model.row:
                    return [
                        DataValue(
                            type=model.cuba_type,
                            value=float(row[model.column])
                        )
                    ]
                else:
                    break

            raise IndexError("Could not find specified data.")

    def slots(self, model):
        return (
            (),
            (
                Slot(type=model.cuba_type),
            )
        )
