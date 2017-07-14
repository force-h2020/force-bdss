from traits.has_traits import HasStrictTraits
from traits.trait_types import String, Dict


class DataSource(HasStrictTraits):
    name = String()
    model_data = Dict()

    @classmethod
    def from_json(cls, json_data):
        self = cls(
            name=json_data["name"],
            model_data=json_data["model_data"]
        )

        return self
