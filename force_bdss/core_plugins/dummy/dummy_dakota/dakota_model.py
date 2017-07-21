from traits.api import List, String
from force_bdss.api import BaseMCOModel


class DummyDakotaModel(BaseMCOModel):
    value_types = List(String)
