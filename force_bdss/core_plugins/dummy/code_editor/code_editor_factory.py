from traits.api import String

from force_bdss.api import factory_id, BaseDataSourceFactory

from .code_editor_model import CodeEditorModel
from .code_editor_data_source import CodeEditorDataSource


class CodeEditorFactory(BaseDataSourceFactory):
    id = String(factory_id("enthought", "code_editor"))

    name = String("Code editor")

    def create_model(self, model_data=None):
        if model_data is None:
            model_data = {}

        return CodeEditorModel(self, **model_data)

    def create_data_source(self):
        return CodeEditorDataSource(self)
