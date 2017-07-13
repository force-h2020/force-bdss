from traits.api import HasStrictTraits, Instance, String, List

from .multi_criteria_optimization import MultiCriteriaOptimization


class Workflow(HasStrictTraits):
    name = String()
    multi_criteria_optimization = Instance(MultiCriteriaOptimization)
    data_sources = List(String)

    @classmethod
    def from_json(cls, json_data):
        self = cls(
            multi_criteria_optimization=MultiCriteriaOptimization.from_json(
                    json_data["multi_criteria_optimization"]
            ),
            data_sources=json_data["data_sources"]
            )

        return self
