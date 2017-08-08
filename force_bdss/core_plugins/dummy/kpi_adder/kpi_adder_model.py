from traits.api import String, on_trait_change

from force_bdss.api import BaseKPICalculatorModel


class KPIAdderModel(BaseKPICalculatorModel):
    cuba_type_in = String()
    cuba_type_out = String()

    @on_trait_change("cuba_type_in,cuba_type_out")
    def _notify_slots_changed(self):
        self.changes_slots = True
