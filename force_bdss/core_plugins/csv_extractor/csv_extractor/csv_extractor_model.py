from traits.api import Int, String

from force_bdss.data_sources.base_data_source_model import BaseDataSourceModel


class CSVExtractorModel(BaseDataSourceModel):
    filename = String()
    row = Int()
    column = Int()
    cuba_type = String()

    @classmethod
    def from_json(cls, json_data):
        return cls(
            filename=json_data["filename"],
            row=json_data["row"],
            column=json_data["column"],
            cuba_type=json_data["cuba_type"]
        )
