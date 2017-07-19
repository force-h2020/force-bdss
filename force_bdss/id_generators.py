import six


def bundle_id(producer, identifier):
    """Creates an id for the bundle.

    Parameters
    ----------
    producer: str
        the company or research institute unique identifier (e.g. "enthought")
    identifier: str
        A unique identifier for the bundle. The producer has authority and
        control over the uniqueness of this identifier.

    Returns
    -------
    str: an identifier to be used in the bundle.
    """
    def is_valid(entry):
        return (
            isinstance(entry, six.string_types) and
            " " not in entry and
            len(entry) != 0)

    if not all(map(is_valid, [producer, identifier])):
        raise ValueError("Invalid parameters specified.")

    return "force.bdss.bundles.{}.{}".format(producer, identifier)
