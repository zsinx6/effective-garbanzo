from django.core.exceptions import ValidationError


class CallIdDuplicationError(ValidationError):
    pass


class InvalidPhoneNumberError(ValidationError):
    pass


class InvalidDateError(ValidationError):
    pass
