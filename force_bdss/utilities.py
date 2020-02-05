def pop_recursive(dictionary, remove_key):
    """Recursively remove a named key from dictionary and any contained
    dictionaries."""
    try:
        dictionary.pop(remove_key)
    except KeyError:
        pass

    for key, value in dictionary.items():
        # If remove_key is in the dict, remove it
        if isinstance(value, dict):
            pop_recursive(value, remove_key)
        # If we have a non-dict iterable which contains a dict,
        # call pop.(remove_key) from that as well
        elif isinstance(value, (tuple, list)):
            for element in value:
                if isinstance(element, dict):
                    pop_recursive(element, remove_key)

    return dictionary


def pop_dunder_recursive(dictionary):
    """ Recursively removes all dunder keys from a nested dictionary. """
    keys = [key for key in dictionary.keys()]
    for key in keys:
        if key.startswith("__") and key.endswith("__"):
            dictionary.pop(key)

    for key, value in dictionary.items():
        # Check subdicts for dunder keys
        if isinstance(value, dict):
            pop_dunder_recursive(value)
        # If we have a non-dict iterable which contains a dict,
        # remove dunder keys from that too
        elif isinstance(value, (tuple, list)):
            for element in value:
                if isinstance(element, dict):
                    pop_dunder_recursive(element)

    return dictionary


def nested_getstate(state_dict):
    # We safely attempt to get the state of the nested objects in `state_dict`
    # on the zero and first levels using __getstate__.
    # If the `state_dict` item is an iterable, we __getstate__ of the iterable
    # elements. Otherwise, we __getstate__ the item itself.
    # If we can't __getstate__ of the item, we leave it as it is.
    for key in state_dict:
        try:
            if isinstance(state_dict[key], (tuple, list)):
                state_dict[key] = [el.__getstate__() for el in state_dict[key]]
            elif isinstance(state_dict[key], dict):
                for element in state_dict[key]:
                    state_dict[key][element] = state_dict[key][
                        element
                    ].__getstate__()
            else:
                state_dict[key] = state_dict[key].__getstate__()
        except AttributeError:
            pass
    return state_dict
