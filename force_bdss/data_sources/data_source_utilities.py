from logging import getLogger

logger = getLogger(__name__)


def merge_trait(source, target, name):
    """Performs a merge of trait `name` between source and target
    HasTrait objects. This is achieved by assigning the source
    attribute onto the target if it has a non-default value.
    Otherwise, the target attribute is assigned onto the
    source.

    Parameters
    ----------
    source, target: objects
        Object instances to have attributes merged
    name: str
        Name of an attribute to check
    """

    if getattr(source, name) == source.trait(name).default:
        setattr(source, name, getattr(target, name))
    else:
        setattr(target, name, getattr(source, name))


def trait_similarity_check(source, target, name, ignore_default=False):
    """Check whether attribute on target can be considered similar
    to the same attribute on source.

    This is allowed either if both attributes share the
    same value, or when ignore_default==True, then it is also allowed
    if either the source or target attribute has not been changed
    from its default value.

    Parameters
    ----------
    source, target: objects
        Object instances to have attributes compared
    name: str
        Name of an attribute to check
    ignore_default: bool, optional, default: False
        Whether or not to ignore the attribute on source or target
        if it is equal to its default value. Note: this will not be
        performed if attribute does not have a default.
    """

    source_attr = getattr(source, name)
    target_attr = getattr(target, name)

    # If ignore_default perform a check to see whether attribute on
    # source or target is its default value, and skip cross check if so
    if ignore_default:
        try:
            source_default_check = (
                source_attr == source.trait(name).default
            )
            target_default_check = (
                target_attr == target.trait(name).default
            )
            if source_default_check or target_default_check:
                return True
        except AttributeError:
            pass

    # Return attribute equality check
    return target_attr == source_attr


def attr_checker(source, target, attributes, ignore_default=False):
    """Performs a `trait_similarity_check` between source and target
    objects for each attribute listed in `attributes`. Returns a list
    of attributes that fail this check.

    Parameters
    ----------
    source, target: objects
        Object instances to perform attribute checks on
    attributes: str or list of str
        An attribute or list of attributes used to check merge
        eligibility of source and target objects
    ignore_default: bool, optional, default: False
        Whether or not to ignore any attributes on source or target
        that are are equal to their default values

    Returns
    -------
    failed_attr: list of str
        Names of attributes on source and target that fail a
        merge check
    """

    # Ensure attributes argument is in an iterable format
    if attributes is None:
        attributes = []
    elif isinstance(attributes, str):
        attributes = [attributes]
    else:
        attributes = list(attributes)

    failed_attr = []

    # Iterate through attributes list
    for attr_name in attributes:
        if not trait_similarity_check(
                source, target,
                attr_name, ignore_default):
            failed_attr.append(attr_name)

    return failed_attr


def merge_trait_with_check(source, target, name, attributes=None,
                           ignore_default=False):
    """Performs the same function as `merge_trait` method, but with
    some extra logic checks on default values and any selected
    attributes supplied by `attributes` argument. These checks are
    designed to determine whether both objects possess a similar
    enough state to merge the `name` attribute.

    Parameters
    ----------
    source, target: HasTraits
        HasTraits instances to have an attribute synchronised
    name: str
        Name of an attribute on both source and target to be synced
    attributes: str or list of str, optional
        An attribute or list of attributes to check equivalence on both
        source and target objects
    ignore_default: bool, optional, default: False
        Whether or not to ignore any attributes on source or target
        that are are equal to their default values

    Raises
    -----
    RuntimeError, if any attribute checks fail
    """

    # Obtain names of any attributes in `attr_check` on both source and
    # target that fail a `trait_similarity_check`
    failed_attr = attr_checker(source, target, attributes,
                               ignore_default=ignore_default)

    if failed_attr:
        attr_name = failed_attr[0]
        error_msg = (
            "Source object has failed a trait "
            "similarity check with target: "
            "The {} attribute of source ({}) doesn't match "
            "target ({}).".format(
                attr_name,
                getattr(source, attr_name),
                getattr(target, attr_name)
            )
        )
        logger.exception(error_msg)
        raise RuntimeError(error_msg)

    # Merge attribute `name` between source and target
    merge_trait(source, target, name)


def merge_lists_with_check(new_list, old_list, attributes):
    """Perform a merge_trait_with_check of each attribute in
    `attributes` between the corresponding elements of new_list
    and old_list. Overwrite priority is given to the values in
    new_list and all current attributes must be similar enough
    to pass a trait_similarity_check

    Parameters
    ----------
    new_list: list
        List of new elements
    old_list: list
        List of old elements to be retained
    attributes: str or list of str, optional
        An attribute or list of attributes to both merge and
        check similarity on each corresponding element in
        new_list and old_list
    ignore_default: bool, optional, default: False
        Whether or not to ignore any attributes on source or target
        that are are equal to their default values
    """

    # Perform a merge_trait_with_check on each corresponding
    # element of new_list and old_list
    for new_element, old_element in zip(new_list, old_list):
        for attr in attributes:
            merge_trait_with_check(
                new_element, old_element, attr, attributes,
                ignore_default=True
            )
