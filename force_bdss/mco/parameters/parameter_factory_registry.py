from traits.api import HasStrictTraits, Dict


class ParameterFactoryRegistry(HasStrictTraits):
    factories = Dict()

    def get_factory_by_id(self, id):
        return self.factories[id]

    def register(self, factory):
        self.factories[factory.id] = factory
