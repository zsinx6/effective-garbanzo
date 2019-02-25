from django.utils import timezone
from django.core.exceptions import ValidationError

from factories import StartCallRecordFactory, EndCallRecordFactory
from records.exceptions import (CallIdDuplicationError, InvalidDateIntervalError,
                                SourceEqualsDestinationError, StartEndError)
import pytest
import datetime


pytestmark = pytest.mark.django_db


def test_source_eq_destination():
    with pytest.raises(SourceEqualsDestinationError):
        StartCallRecordFactory(source="1111111111", destination="1111111111")


def test_start_source():
    with pytest.raises(StartEndError):
        StartCallRecordFactory(source=None)


def test_start_destination():
    with pytest.raises(StartEndError):
        StartCallRecordFactory(destination=None)


def test_start_no_phone():
    with pytest.raises(StartEndError):
        StartCallRecordFactory(source=None, destination=None)


def test_start():
    assert StartCallRecordFactory()


def test_end_source():
    with pytest.raises(StartEndError):
        EndCallRecordFactory(source="1111111111")


def test_end_destination():
    with pytest.raises(StartEndError):
        EndCallRecordFactory(destination="1111111111")


def test_end():
    assert EndCallRecordFactory()


def test_invalid_phone_number_alpha():
    with pytest.raises(ValidationError):
        StartCallRecordFactory(source="this is not a number")


def test_invalid_phone_number_short():
    with pytest.raises(ValidationError):
        StartCallRecordFactory(source="123")


def test_invalid_phone_number_long():
    with pytest.raises(ValidationError):
        StartCallRecordFactory(source="123456789123456789")


def test_duplicate_call_id():
    assert StartCallRecordFactory()
    assert EndCallRecordFactory()
    with pytest.raises(CallIdDuplicationError):
        StartCallRecordFactory()


def test_duplicate_start_call_id():
    assert StartCallRecordFactory(call_id=1)
    with pytest.raises(CallIdDuplicationError):
        StartCallRecordFactory(call_id=1)


def test_duplicate_end_call_id():
    assert EndCallRecordFactory(call_id=1)
    with pytest.raises(CallIdDuplicationError):
        EndCallRecordFactory(call_id=1)


def test_end_date_before_start():
    assert EndCallRecordFactory()
    with pytest.raises(InvalidDateIntervalError):
        StartCallRecordFactory(timestamp=timezone.now() + datetime.timedelta(days=1))


def test_start_date_after_end():
    assert StartCallRecordFactory(timestamp=timezone.now() + datetime.timedelta(days=1))
    with pytest.raises(InvalidDateIntervalError):
        EndCallRecordFactory()


def test_start_end_correct():
    assert StartCallRecordFactory()
    assert EndCallRecordFactory(timestamp=timezone.now() + datetime.timedelta(days=1))
