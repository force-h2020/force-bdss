from traits.api import HasStrictTraits, String


class KPIAdderModel(HasStrictTraits):
    cuba_type_in = String()
    cuba_type_out = String()

    @classmethod
    def from_json(cls, json_data):
        return cls(
            cuba_type_in=json_data["cuba_type_in"],
            cuba_type_out=json_data["cuba_type_out"]
        )
