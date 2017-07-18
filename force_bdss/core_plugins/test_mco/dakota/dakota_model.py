from traits.api import List, String

from force_bdss.mco.base_mco_model import BaseMCOModel


class DakotaModel(BaseMCOModel):
    value_types = List(String)

    @classmethod
    def from_json(cls, model_data):
        return cls(value_types=model_data["value_types"])
