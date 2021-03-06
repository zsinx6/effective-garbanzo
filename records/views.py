from rest_framework import viewsets, mixins

from records.models import CallRecord
from records.serializers import CallRecordSerializer

from bills.models import BillInformation


class CallRecordViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = CallRecord.objects.all()
    serializer_class = CallRecordSerializer

    def perform_create(self, serializer):
        """Used to insert the BillInformation when there are 2 registers for
        the same call_id. This is the only way for the end user to create a
        BillInformation.
        """

        call_id = self.request.data["call_id"]
        serializer.save()
        other_call_id = self.queryset.filter(call_id=call_id)
        if other_call_id.count() == 2:
            start_call = other_call_id.get(type="start")
            end_call = other_call_id.get(type="end")
            start_timestamp = start_call.timestamp
            end_timestamp = end_call.timestamp
            BillInformation.objects.create(source=start_call, start=start_timestamp, end=end_timestamp)
