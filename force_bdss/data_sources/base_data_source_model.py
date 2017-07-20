from traits.api import ABCHasStrictTraits, Instance

from .i_data_source_bundle import IDataSourceBundle


class BaseDataSourceModel(ABCHasStrictTraits):
    """Base class for the bundle specific DataSource models.
    This model will also provide, through traits/traitsui magic the View
    that will appear in the workflow manager UI.

    In your bundle definition, your bundle-specific model must reimplement
    this class.
    """
    #: A reference to the creating bundle, so that we can
    #: retrieve it as the originating factory.
    bundle = Instance(IDataSourceBundle, visible=False, transient=True)

    def __init__(self, bundle, *args, **kwargs):
        self.bundle = bundle
        super(BaseDataSourceModel, self).__init__(*args, **kwargs)
