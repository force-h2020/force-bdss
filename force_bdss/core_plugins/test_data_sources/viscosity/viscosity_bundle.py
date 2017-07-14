from traits.api import provides, HasStrictTraits, String

from force_bdss.data_sources.i_data_source_bundle import IDataSourceBundle

from .viscosity_data_source import ViscosityDataSource
from .viscosity_model import ViscosityModel


@provides(IDataSourceBundle)
class ViscosityBundle(HasStrictTraits):
    name = String("viscosity")

    def create_model(self, model_data):
        return ViscosityModel.from_json(model_data)

    def create_ui(self):
        pass

    def create_data_source(self, application, model):
        return ViscosityDataSource(self, application, model)
