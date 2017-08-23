from traits.api import Code, Int, on_trait_change, List, Str, Button

from force_bdss.api import BaseDataSourceModel


class CodeEditorModel(BaseDataSourceModel):
    code = Code()

    nb_inputs = Int()
    nb_outputs = Int()

    input_types = List(Str)
    output_types = List(Str)

    load_button = Button('Load python script')

    @on_trait_change('nb_inputs,nb_outputs', post_init=True)
    def update_slot_sizes(self):
        self.input_types = ['' for _ in range(self.nb_inputs)]
        self.output_types = ['' for _ in range(self.nb_outputs)]
        self.changes_slots = True

    @on_trait_change('input_types[],output_types[]')
    def update_slot_types(self):
        self.changes_slots = True

    @on_trait_change('load_button')
    def load_python_script(self):
        from pyface.api import FileDialog, OK, error

        dialog = FileDialog(
            action="open",
            wildcard='Python files (*.py)|*.py|'
        )

        result = dialog.open()

        if result is not OK:
            return

        try:
            with open(dialog.path, 'r') as fobj:
                self.code = fobj.read()
        except IOError as e:
            error(
                None,
                "Oups ! Something went wrong when "
                "opening the file {}: \n{}".format(
                    dialog.path, str(e)
                )
            )

    def default_traits_view(self):
        from traitsui.api import View, Item, UItem, HGroup

        return View(
            HGroup(
                Item('nb_inputs', label='Number'),
                Item('input_types', label='Types'),
                label='Inputs',
                show_border=True,
            ),
            HGroup(
                Item('nb_outputs', label='Number'),
                Item('output_types', label='Types'),
                label='Outputs',
                show_border=True,
            ),
            UItem('load_button'),
            Item('code'),
            buttons=['OK', 'Cancel'],
        )

    def _code_default(self):
        return (
            "# You can import any module you want which is installed in\n "
            "# your environment:\n"
            "#\n"
            "import math\n"
            "#\n"
            "# You have access to the input parameters you defined in the\n"
            "# tree editor of the Workflow (e.g. if you set \"p1\" as an \n"
            "# input for this data source, you have access to \"p1\" value\n"
            "# in the scope of this code)\n"
            "#\n"
            "# You must set all the values you defined as ouput of this data\n"
            "# source inside this code (e.g. if you set \"p_out\" as an\n"
            "# output of this data source, you must set a value for\n"
            "# \"p_out\" inside of this code\n"
        )
