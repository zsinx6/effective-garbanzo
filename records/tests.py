import datetime

from django.test import TestCase
from django.utils import timezone

from .models import CallRecord


class CallRecordModelTests(TestCase):

    phone1 = "19989686516"
    phone2 = "1934634678"

    def test_source_eq_destination(self):
        bad_record = CallRecord(type="start", timestamp=timezone.now(),
                                call_id=1, source=self.phone1, destination=self.phone1)


