from traits.api import HasStrictTraits, Dict, String

from force_bdss.mco.parameters.base_mco_parameter_factory import \
    BaseMCOParameterFactory


class MCOParameterFactoryRegistry(HasStrictTraits):
    """Registry to keep the parameter factories and lookup them.
    """
    # Temp: this will become an extension point.
    factories = Dict(String, BaseMCOParameterFactory)

    def get_factory_by_id(self, bundle_id, parameter_factory_id):
        """Finds the factory by its id, so that we can obtain it as from
        the id in the model file.
        """
        return self.factories[(bundle_id, parameter_factory_id)]

    def register(self, factory):
        """Registers a new factory"""
        self.factories[(factory.bundle.id, factory.id)] = factory
