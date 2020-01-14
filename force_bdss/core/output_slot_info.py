from .base_slot_info import BaseSlotInfo


class OutputSlotInfo(BaseSlotInfo):
    """
    Class that specifies the name and characteristics of the output slots
    of a data source.
    """

    def verify(self):
        return self._verify_name("Output Slot", "warning")
