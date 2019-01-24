from rest_framework.exceptions import ValidationError


class CallIdDuplicationError(ValidationError):
    pass


class StartEndError(ValidationError):
    pass


class InvalidDateIntervalError(ValidationError):
    pass


class SourceEqualsDestinationError(ValidationError):
    pass
