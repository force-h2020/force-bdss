from logging import getLogger

logger = getLogger(__name__)


class TraitSimilarityError(Exception):
    """Reports the failure of a attr_similarity_check."""


def attr_similarity_check(object_a, object_b, name, ignore_default=False):
    """Check whether attribute on object_a can be considered similar
    to the same attribute on object_b.

    This is allowed either if both attributes share the
    same `name` value, or when ignore_default==True, then it is also
    allowed if either attribute has not been changed from its default
    value.

    Parameters
    ----------
    object_a, object_b: objects
        Object instances to have attributes compared
    name: str
        Name of an attribute to check
    ignore_default: bool, optional, default: False
        Whether or not to ignore the attribute on source or target
        if it is equal to its default value. Note: this will not be
        performed if attribute does not have a default.
    """

    attr_a = getattr(object_a, name)
    attr_b = getattr(object_b, name)

    # If ignore_default perform a check to see whether attribute on
    # either object is its default value, and skip cross check if so
    if ignore_default:
        try:
            default_check_a = (
                attr_a == object_a.trait(name).default
            )
            default_check_b = (
                attr_b == object_b.trait(name).default
            )
            if default_check_a or default_check_b:
                return True
        except AttributeError:
            # If either object does not have a default attribute, ignore
            # this step
            pass

    # Return attribute equality check
    return attr_a == attr_b


def attr_checker(object_a, object_b, attributes, ignore_default=False):
    """Performs a `attr_similarity_check` between source and target
    objects for each attribute listed in `attributes`. Returns a list
    of attribute names that fail this check.

    Parameters
    ----------
    object_a, object_b: objects
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
        if not attr_similarity_check(
                object_a, object_b,
                attr_name, ignore_default):
            failed_attr.append(attr_name)

    return failed_attr


def merge_trait(source, target, name):
    """Performs a merge of trait `name` between source and target
    HasTrait objects. This is achieved by assigning the source
    attribute onto the target if it has a non-default value.
    Otherwise, the target attribute is assigned onto the
    source.

    The result is that both source and target have the
    same value for their `name` attribute

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


def merge_trait_with_check(source, target, attributes, ignore_default=True):
    """Performs the same function as `merge_trait` method, but with
    some extra logic checks on default values and any selected
    attributes supplied by `attributes` argument. These checks are
    designed to determine whether both objects possess a similar
    enough state to merge their attributes.

    Parameters
    ----------
    source, target: HasTraits
        HasTraits instances to have thier attributes merged
    attributes: str or list of str
        An attribute or list of attributes to merge on both
        source and target objects
    ignore_default: bool, optional, default: True
        Whether or not to ignore any attributes on source or target
        during the attr_checker that are are equal to their default values

    Raises
    -----
    TraitSimilarityError, if any attribute checks fail
    """

    # Obtain names of any provided attributes on both source and
    # target that fail an `attr_similarity_check`
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
        raise TraitSimilarityError(error_msg)

    # Merge attributes between source and target
    if isinstance(attributes, str):
        merge_trait(source, target, attributes)
    else:
        for attr in attributes:
            merge_trait(source, target, attr)
