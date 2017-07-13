from traits.api import provides, HasStrictTraits, String

from force_bdss.data_sources.i_data_source import (
    IDataSource)


@provides(IDataSource)
class Price(HasStrictTraits):
    computes = String("price")

    def run(self, workflow):
        print("Computing price")
