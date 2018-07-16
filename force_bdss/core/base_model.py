from traits.api import ABCHasStrictTraits, Instance

from force_bdss.core.base_factory import BaseFactory


class BaseModel(ABCHasStrictTraits):
    """Base class for all the models of all the factories."""

    #: A reference to the creating factory, so that we can
    #: retrieve it as the originating factory.
    factory = Instance(BaseFactory, visible=False, transient=True)

    def __init__(self, factory, *args, **kwargs):
        super(BaseModel, self).__init__(factory=factory, *args, **kwargs)
