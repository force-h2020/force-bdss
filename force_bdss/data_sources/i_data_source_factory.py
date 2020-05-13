#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Type

from force_bdss.core.i_factory import IFactory


class IDataSourceFactory(IFactory):
    """Envisage required interface for the BaseDataSourceFactory.
    You should not need to use this directly.

    Refer to the BaseDataSourceFactory for documentation.
    """
    data_source_class = Type(
        "force_bdss.data_sources.base_data_source.BaseDataSource",
        allow_none=False
    )

    model_class = Type(
        "force_bdss.data_sources.base_data_source_model.BaseDataSourceModel",
        allow_none=False
    )

    def get_data_source_class(self):
        """
        :return: data source class.
        """

    def get_model_class(self):
        """
        :return: model class.
        """

    def create_data_source(self):
        """Returns an instance of subclass BaseDataSource
        """

    def create_model(self):
        """Returns an instance of subclass BaseDataSourceModel
        """
