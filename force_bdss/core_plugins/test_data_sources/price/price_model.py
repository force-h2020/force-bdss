from traits.has_traits import HasStrictTraits


class PriceModel(HasStrictTraits):
    @classmethod
    def from_json(cls, model_data):
        return cls()
