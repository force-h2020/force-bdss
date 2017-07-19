from traits.api import Int, String

from force_bdss.api import BaseDataSourceModel


class CSVExtractorModel(BaseDataSourceModel):
    filename = String()
    row = Int()
    column = Int()
    cuba_type = String()
