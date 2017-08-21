from traits.api import Code

from force_bdss.api import BaseDataSourceModel


class CodeEditorModel(BaseDataSourceModel):
    code = Code()
