from traits.api import List, String
from force_bdss.api import BaseMCOModel


class DakotaModel(BaseMCOModel):
    value_types = List(String)
