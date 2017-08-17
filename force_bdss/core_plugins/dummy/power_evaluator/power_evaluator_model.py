from traits.api import Float, String, on_trait_change

from force_bdss.api import BaseDataSourceModel


class PowerEvaluatorModel(BaseDataSourceModel):
    power = Float()
    cuba_type_in = String()
    cuba_type_out = String()

    @on_trait_change("cuba_type_in,cuba_type_out")
    def _notify_changes_slots(self):
        self.changes_slots = True
