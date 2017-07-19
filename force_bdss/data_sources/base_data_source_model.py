from traits.api import ABCHasStrictTraits, Instance

from .i_data_source_bundle import IDataSourceBundle


class BaseDataSourceModel(ABCHasStrictTraits):
    bundle = Instance(IDataSourceBundle, visible=False, transient=True)

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseDataSourceModel, self).__init__(*args, **kwargs)
