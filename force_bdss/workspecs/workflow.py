from traits.api import HasStrictTraits, Instance, String

from .multi_criteria_optimization import MultiCriteriaOptimization


class Workflow(HasStrictTraits):
    name = String()
    multi_criteria_optimization = Instance(MultiCriteriaOptimization)

    @classmethod
    def from_json(cls, json_data):
        self = cls(
            multi_criteria_optimization=MultiCriteriaOptimization.from_json(
                    json_data["multi_criteria_optimization"]
                )
            )

        return self
