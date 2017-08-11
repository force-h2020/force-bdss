from traits.api import Int, String, on_trait_change, File

from force_bdss.api import BaseDataSourceModel


class CSVExtractorModel(BaseDataSourceModel):
    filename = File()
    row = Int()
    column = Int()
    cuba_type = String()

    @on_trait_change("cuba_type")
    def _notify_changes_slots(self):
        self.changes_slots = True
