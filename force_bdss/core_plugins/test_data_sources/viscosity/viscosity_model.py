from traits.api import HasStrictTraits


class ViscosityModel(HasStrictTraits):
    @classmethod
    def from_json(cls, model_data):
        return cls()
