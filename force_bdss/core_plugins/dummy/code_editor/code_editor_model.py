from traits.api import Code, Int, on_trait_change

from force_bdss.api import BaseDataSourceModel


class CodeEditorModel(BaseDataSourceModel):
    code = Code()

    nb_inputs = Int()
    nb_outputs = Int()

    @on_trait_change('nb_inputs,nb_outputs')
    def update_slots(self):
        self.changes_slots = True
