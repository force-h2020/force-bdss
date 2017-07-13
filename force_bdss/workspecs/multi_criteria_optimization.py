from traits.api import HasStrictTraits, String


class MultiCriteriaOptimization(HasStrictTraits):
    name = String()

    @classmethod
    def from_json(cls, json_data):
        self = cls(
            name=json_data["name"]
        )

        return self
