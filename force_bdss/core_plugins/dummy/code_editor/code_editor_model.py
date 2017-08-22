from traits.api import Code, Int, on_trait_change, List, Str

from force_bdss.api import BaseDataSourceModel


class CodeEditorModel(BaseDataSourceModel):
    code = Code()

    nb_inputs = Int()
    nb_outputs = Int()

    input_types = List(Str)
    output_types = List(Str)

    @on_trait_change('nb_inputs,nb_outputs')
    def update_slot_sizes(self):
        self.input_types = ['' for _ in range(self.nb_inputs)]
        self.output_types = ['' for _ in range(self.nb_outputs)]
        self.changes_slots = True

    @on_trait_change('input_types[],output_types[]')
    def update_slot_types(self):
        self.changes_slots = True
