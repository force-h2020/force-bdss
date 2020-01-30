from copy import deepcopy
import importlib
import json

from traits.api import (
    HasStrictTraits,
    List,
    Instance,
    Float,
    Unicode,
    TraitError,
)

from force_bdss.core.data_value import DataValue
from force_bdss.core.base_model import pop_dunder_recursive, nested_getstate


class DriverEventTypeError(TypeError):
    """Raised when a BaseDriverEvent is attempted to be instantiated with a
     class that is not a subclass of BaseDriverEvent."""


class DriverEventDeserializationError(TypeError):
    """Raised when a BaseDriverEvent is attempted to be instantiated with a
     class that is not a subclass of BaseDriverEvent."""


class BaseDriverEvent(HasStrictTraits):
    """ Base event for the MCO driver."""

    def __getstate__(self):
        """ Returns state dictionary of the object. For a nested dict,
        __getstate__ is applied to zero level items and first level items.
        """
        state = pop_dunder_recursive(super().__getstate__())
        state = nested_getstate(state)
        id = ".".join((self.__class__.__module__, self.__class__.__name__))
        state = {"model_data": state, "id": id}
        return state

    def dumps_json(self):
        return json.dumps(self.__getstate__())

    @staticmethod
    def get_event_class(id_string):
        """Retrieve the class object from the id_string

        Parameters
        ----------
        id_string: str
            The string containing the path to the class definition.

        Returns
        -------
        cls: BaseDriverEvent subclass

        Raises
        ------
        ImportError
            If the path from the `id_string` is an incorrect
             reference
        DriverEventTypeError
            If the class from the `id_string` is not a subclass of
            BaseDriverEvent
        """
        class_module, class_name = id_string.rsplit(".", 1)
        module = importlib.import_module(class_module)
        try:
            cls = getattr(module, class_name)
        except AttributeError:
            error_message = (
                f"Unable to locate the class definition {class_name} "
                f"in module {module} requested by the event with "
                f"id {id_string}"
            )
            raise ImportError(error_message)
        if not issubclass(cls, BaseDriverEvent):
            raise DriverEventTypeError(
                f"Class {cls} must be a subclass of BaseDriverEvent"
            )
        return cls

    @classmethod
    def from_json(cls, json_data):
        """ Instantiate a BaseDriverEvent object from a `json_data`
        dictionary and the generating `factory_registry`.
        If the `json_data` is an empty dict, the `data_sources`
        attribute will be an empty list.

        First, the method attempts to create an instance by passing
        the json_data["model_data"] data to the default traits init
        method (as a dictionary). If the attributes of the new instance
        can't be initialized that way (for instance, if they are custom
        traits objects themselves), the method uses the `klass.from_json`
        method. If this was not successful, an Exception is raised.

        Parameters
        ----------
        json_data: dict
            Dictionary with an execution layer serialized data

        Returns
        ----------
        event: BaseDriverEvent
            BaseDriverEvent or a subclass of BaseDriverEvent instance
            with attributes values from the `json_data` dict
        """
        try:
            class_id = json_data["id"]
        except Exception as e:
            raise DriverEventDeserializationError(
                "Could not parse json data: {}".format(e)
            )
        klass = cls.get_event_class(class_id)
        try:
            event = klass(**json_data["model_data"])
        except TraitError:
            try:
                event = klass.from_json(json_data["model_data"])
            except Exception:
                error_message = (
                    f"Unable to instantiate a {klass} instance "
                    f"with data {json_data['model_data']}: the "
                    f"`__init__` and `from_json` methods failed "
                    f"to create an instance."
                )
                raise DriverEventDeserializationError(error_message)

        return event

    @classmethod
    def loads_json(cls, data):
        json_data = json.loads(data)
        return cls.from_json(json_data)


class MCOStartEvent(BaseDriverEvent):
    """ The MCO driver should emit this event when the evaluation starts."""

    #: The names assigned to the parameters.
    parameter_names = List(Unicode())

    #: The names associated to the KPIs
    kpi_names = List(Unicode())

    def serialize(self):
        """ Provides serialized form of MCOStartEvent for further data storage
        (e.g. in csv format) or processing.


        Usage example:
        For a custom MCOStartEvent subclass, this method can be overloaded.
        An example of a custom `serialize` method would be:
        >>> class CustomMCOStartEvent(MCOStartEvent):
        >>>
        >>>     def serialize(self):
        >>>         custom_data = [f"{name} data" for name in self.kpi_names]
        >>>         return super().serialize() + custom_data
        >>>

        Returns:
            List(Unicode): event parameters names and kpi names
        """
        return self.parameter_names + self.kpi_names


class WeightedMCOStartEvent(MCOStartEvent):
    """Initializes reporting of weights generated during an MCO by a
    WeightedOptimizerEngine"""

    def serialize(self):
        """Overloaded method to provide weights alongside each
        reported KPI"""
        value_names = self.parameter_names
        for kpi_name in self.kpi_names:
            value_names.extend([kpi_name, kpi_name + " weight"])
        return value_names


class MCOFinishEvent(BaseDriverEvent):
    """ The MCO driver should emit this event when the evaluation ends."""


class MCOProgressEvent(BaseDriverEvent):
    """ The MCO driver should emit this event for every new point that is
    evaluated during the MCO run.
    """

    #: The point in parameter space resulting from the pareto
    #: front optimization
    optimal_point = List(Instance(DataValue))

    #: The associated KPIs to the above point
    optimal_kpis = List(Instance(DataValue))

    def serialize(self):
        """ Provides serialized form of MCOProgressEvent for further data storage
        (e.g. in csv format) or processing.

        Usage example:
        For a custom MCOProgressEvent subclass, this method can be overloaded.
        An example of a custom `serialize` method would be:
        >>> class CustomMCOProgressEvent(MCOProgressEvent):
        >>>     metadata = List(Float)
        >>>     def serialize(self):
        >>>         return super().serialize() + self.metadata
        >>>

        Returns:
            List(Datavalue.value): values of the event optimal points and kpis
        """
        event_datavalues = self.optimal_point + self.optimal_kpis
        return [entry.value for entry in event_datavalues]

    @classmethod
    def from_json(cls, json_data):
        data = deepcopy(json_data)
        data["optimal_point"] = [
            DataValue(**data) for data in data["optimal_point"]
        ]
        data["optimal_kpis"] = [
            DataValue(**data) for data in data["optimal_kpis"]
        ]
        return cls(**data)


class WeightedMCOProgressEvent(MCOProgressEvent):
    """Allows reporting of weights generated during an MCO by a
    WeightedOptimizerEngine"""

    #: Weights assigned to each KPI during the MCO optimization
    weights = List(Float())

    def _weights_default(self):
        """Default weights are normalised and uniform for each KPI"""
        if self.optimal_kpis:
            return [1 / len(self.optimal_kpis)] * len(self.optimal_kpis)
        return []

    def serialize(self):
        """Overloaded method to provide weights alongside each
        reported KPI"""
        event_datavalues = [entry.value for entry in self.optimal_point]
        for kpi, weight in zip(self.optimal_kpis, self.weights):
            event_datavalues.extend([kpi.value, weight])
        return event_datavalues
