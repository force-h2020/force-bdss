from traits.api import HasStrictTraits, String, Dict


class KPICalculator(HasStrictTraits):
    id = String()
    model_data = Dict()

    @classmethod
    def from_json(cls, json_data):
        self = cls(
            id=json_data["id"],
            model_data=json_data["model_data"]
        )

        return self
