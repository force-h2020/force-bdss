from traits.api import HasStrictTraits


class DakotaModel(HasStrictTraits):
    @classmethod
    def from_json(cls, model_data):
        return cls()
