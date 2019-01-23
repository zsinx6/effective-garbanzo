import factory

from records.models import CallRecord
from django.utils import timezone


class StartCallRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CallRecord

    type = "start"
    timestamp = timezone.now()
    call_id = "20"
    source = "11888652365"
    destination = "1256785412"


class EndCallRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CallRecord

    type = "end"
    timestamp = timezone.now()
    call_id = "20"
