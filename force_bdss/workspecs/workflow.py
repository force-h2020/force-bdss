from traits.api import HasStrictTraits, Instance, String, List

from .multi_criteria_optimization import MultiCriteriaOptimization


class Workflow(HasStrictTraits):
    name = String()
    multi_criteria_optimization = Instance(MultiCriteriaOptimization)
    key_performance_indicators = List(String)

    @classmethod
    def from_json(cls, json_data):
        self = cls(
            multi_criteria_optimization=MultiCriteriaOptimization.from_json(
                    json_data["multi_criteria_optimization"]
            ),
            key_performance_indicators=json_data["key_performance_indicators"]
            )

        return self
