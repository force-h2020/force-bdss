from traits.api import provides, HasStrictTraits, String

from force_bdss.data_sources.i_data_source import (
    IDataSource)


@provides(IDataSource)
class Basic(HasStrictTraits):
    computes = String("basic")

    def run(self, workflow):
        print("Computing basic key performance indicator, {}".format(workflow))
