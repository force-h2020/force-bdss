#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import importlib
import json

from traits.api import HasStrictTraits, TraitError

from force_bdss.utilities import pop_dunder_recursive, nested_getstate


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
        """ Returns the state of the BaseDriverEvent subclass instance,
        serialized to a json-formatted string.

        Returns
        ----------
        JSON-formatted string
        """
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
        except KeyError as e:
            raise DriverEventDeserializationError(
                f"Could not parse json data. "
                f"The `json_data` argument should contain the"
                f"class id key {e}."
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
        """ Create a BaseDriverEvent subclass object from a json loadable
        `data` object.

        Parameters
        ----------
        data: `str`, `bytes` or `bytearray`
            An object to be json.loads-ed and passed to class constructor
        """
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError as e:
            raise DriverEventDeserializationError(
                f"Data object {data} is not compatible "
                f"with the json.loads method and raises {e}"
            )
        return cls.from_json(json_data)
