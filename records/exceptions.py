"""Exceptions used in records.models.CallRecord to make the usage errors and
code organization more clear.
"""

from rest_framework.exceptions import ValidationError


class CallIdDuplicationError(ValidationError):
    """Used when the call_id is already used or when the same call_id is used
    for more than one start or end records.
    """


class StartEndError(ValidationError):
    """Used when the the start record does not have source and destination or
    when the end record have source or destination.
    """


class InvalidDateIntervalError(ValidationError):
    """Used when the start date is later than the end date in a record.
    """


class SourceEqualsDestinationError(ValidationError):
    """Used when the source is the same as the destination number.
    """
