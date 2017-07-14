from traits.api import HasStrictTraits, Int, String


class CSVExtractorModel(HasStrictTraits):
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
