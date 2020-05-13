#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import abc
from traits.api import ABCHasStrictTraits, Instance

from force_bdss.data_sources.i_data_source_factory import IDataSourceFactory


class BaseDataSource(ABCHasStrictTraits):
    """Base class for the DataSource, any computational engine/retriever
    for data.

    Inherit from this class for your specific DataSource.
    """

    #: A reference to the factory
    factory = Instance(IDataSourceFactory)

    def __init__(self, factory, *args, **kwargs):
        super(BaseDataSource, self).__init__(factory=factory, *args, **kwargs)

    def _run(self, model, parameters):
        """ Private method to execute the DataSource from the ExecutionLayer.
        Sends BaseDriverEvent event before and after the DataSource execution,
        such that the Workflow can be interacted with during its execution.
        """
        model.notify_start_event()
        result = self.run(model, parameters)
        model.notify_finish_event()
        return result

    @abc.abstractmethod
    def run(self, model, parameters):
        """
        Executes the Data Source evaluation and returns the results it
        computes. Reimplement this method in your specific DataSource.

        Parameters
        ----------
        model: BaseDataSourceModel
            The model of the DataSource, instantiated through create_model()

        parameters: List(DataValue)
            a list of DataValue objects containing the information needed
            for the execution of the DataSource.

        Returns
        -------
        List(DataValue)
            A list containing the computed Data Values.
        """

    @abc.abstractmethod
    def slots(self, model):
        """Returns the input (and output) slots of the DataSource.
        Slots are the entities that are needed (and produced) by this
        DataSource.

        The slots may depend on the configuration options, and thus the model.
        This allows, for example, to change the slots depending if an option
        is enabled or not.

        Parameters
        ----------
        model: BaseDataSourceModel
            The model of the DataSource, instantiated through create_model()

        Returns
        -------
        (input_slots, output_slots): tuple[tuple, tuple]
            A tuple containing two tuples.
            The first element is the input slots, the second element is
            the output slots. Each slot must be an instance of the Slot class.
            It is possible for each of the two inside tuples to be empty.
            The case of an empty input slot is common: the DataSource does
            not need any information from the MCO to operate.
            The case of an empty output slot is uncommon, but supported:
            the DataSource does not produce any output and is therefore
            useless.
        """
