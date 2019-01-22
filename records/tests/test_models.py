from django.utils import timezone
from django.core.exceptions import ValidationError

from records.exceptions import CallIdDuplicationError, InvalidDateError, InvalidPhoneNumberError
from records.models import CallRecord

import pytest


pytestmark = pytest.mark.django_db


def test_source_eq_destination():
    bad_record = CallRecord(type="start", timestamp=timezone.now(),
                            call_id=1, source="11989686511", destination="11989686511")
    with pytest.raises(InvalidPhoneNumberError):
        bad_record.save()


def test_start_source():
    bad_record = CallRecord(type="start", timestamp=timezone.now(),
                            call_id=1, source="11989686511")
    with pytest.raises(InvalidPhoneNumberError):
        bad_record.save()


def test_start_destination():
    bad_record = CallRecord(type="start", timestamp=timezone.now(),
                            call_id=1, destination="11989686511")
    with pytest.raises(InvalidPhoneNumberError):
        bad_record.save()


def test_start_no_phone():
    bad_record = CallRecord(type="start", timestamp=timezone.now(),
                            call_id=1)
    with pytest.raises(InvalidPhoneNumberError):
        bad_record.save()


def test_start():
    record = CallRecord(type="start", timestamp=timezone.now(),
                        call_id=1, source="16989686518", destination="11989686511")
    with pytest.raises(InvalidPhoneNumberError):
        record.save()


def test_end_source():
    bad_record = CallRecord(type="start", timestamp=timezone.now(),
                            call_id=1, source="11989686511")
    with pytest.raises(InvalidPhoneNumberError):
        bad_record.save()


def test_end_destination():
    bad_record = CallRecord(type="start", timestamp=timezone.now(),
                            call_id=1, destination="11989686511")
    with pytest.raises(InvalidPhoneNumberError):
        bad_record.save()
