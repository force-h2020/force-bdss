from traits.api import HasStrictTraits, List, String


class DakotaModel(HasStrictTraits):
    value_types = List(String)

    @classmethod
    def from_json(cls, model_data):
        return cls(value_types=model_data["value_types"])
