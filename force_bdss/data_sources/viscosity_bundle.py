from traits.api import provides, HasStrictTraits

from force_bdss.data_sources.viscosity_model import ViscosityModel
from .i_data_source_bundle import IDataSourceBundle
from .viscosity_data_source import ViscosityDataSource


@provides(IDataSourceBundle)
class ViscosityBundle(HasStrictTraits):
    def create_model(self, model_data):
        return ViscosityModel.from_json(model_data)

    def create_ui(self):
        pass

    def create_data_source(self, application, model):
        return ViscosityDataSource(self, application, model)
